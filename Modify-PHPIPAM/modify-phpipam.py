#!/usr/bin/python

import phpipamapi
import json
import argparse
import getpass

class PHPIpamModifier:
    """
    Program that creates or deletes items in their respective resource
    """
    def __init__(self, args: argparse.Namespace) -> None:
        self.__server_info, self.__actions = self._read_json(args.filename)

        self.__server_api_call = self._api_call(self.__server_info, args)

        self.__action_choices = {'addresses':{'search':self.__server_api_call.addresses.search,
                                'create':self.__server_api_call.addresses.create,
                                'patch':self.__server_api_call.addresses.patch,
                                'delete':self.__server_api_call.addresses.delete}}

        self._process_actions()

    def _read_json(self, filename: str) -> tuple:
        try:
            with open(filename, "r", encoding="utf-8") as file:
                jcontents = json.load(file)

        except OSError as e:
            print(f"File issue: {e}")

        except ValueError as e:
            print(F"JSON processing issue: {e}")

        return jcontents['server'], jcontents['actions']

    def _api_call(self, server_info: dict, args: argparse.Namespace) -> phpipamapi.Caller:

        try:
            if "key" in server_info and args.password is None and args.username is None:
                return phpipamapi.Caller(server_info['url'], server_info['app'],
                                        api_key=server_info['key'])

            elif args.password is not None and args.username is not None:
                return phpipamapi.Caller(server_info['url'], server_info['app'],
                                        api_user=args.username, api_password=args.password)

            else:
                username = input("API Username: ")
                password = getpass.getpass("API Password: ")

                return phpipamapi.Caller(server_info['url'], server_info['app'],
                                        api_user=username, api_password=password)

        except ExceptionGroup as e:
            print(f"Issue creating api caller: {e}")

    def _read_csv(self, filename: str) -> list[dict]:
        items = []

        with open(filename, "r", encoding="utf-8") as file:
            headers = [header.strip() for header in file.readline().split(',')]

            for line in file:
                items.append({headers[i]:value.strip() for i, value in enumerate(line.split(','))})

        return items

    def _process_actions(self):
        for action in self.__actions.value():
            if action["function"].lower() == "update":
                self._update_items(action)

            elif action["function"].lower() == "delete":
                self._delete_items(action)

            else:
                print("whut")
                raise NotImplementedError(f"Operation {action["function"]} is not implemented, "\
                                          f"options are (update, create)")

    def _update_items(self, action: dict):
        csv_changes = self._read_csv(action['file'])
        result_changes = []

        for item in csv_changes:

            id_exists = "id" in item and (item["id"] is not None or item["id"] != "")

            if id_exists:
                try:
                    return_result = self.__action_choices[action['controller']]['patch'](item['id'], data=item)

                except:
                    print(f"Item: {item}, was unable to complete update")

            elif not id_exists:
                try:
                    return_data = self.__action_choices[action['controller']]['search'](item["ip"])

                    if "id" in return_data and return_data["id"] is not None:
                        item["id"] = return_data["id"]
                        return_result = self.__action_choices[action['controller']]['patch'](item['id'], data=item)

                    else:
                        if "id" in item and (item["id"] is None or item["id"] == ""):
                            item.pop("id")
                        return_result = self.__action_choices[action['controller']]['create'](data=item)

                except:
                    print(f"Item: failed to create {item}")

            try:
                result_changes.append(return_result["data"])

            except:
                print(f"Results missing data: {return_result}")

    def _delete_items(self, action: dict):
        csv_changes = self._read_csv(action['file'])
        result_changes = []

        for item in csv_changes:
            if "id" in item and not (item["id"] is None or item["id"] == ""):
                try:
                    return_result = self.__action_choices[action['controller']]['delete'](item["id"])

                except:
                    print(f"Error deleting ip: {item}")

            else:

                try:
                    return_data = self.__action_choices[action['controller']]['search'](item["ip"])
                    item["id"] = return_data["id"]
                    return_result = self.__action_choices[action['controller']]['delete'](item["id"])

                except:
                    print(f"Error deleting ip: {item}")

            try:
                result_changes.append(return_result["data"])

            except:
                print(f"Results missing data: {return_result}")

if __name__ == "__main__":

    parser = argparse.ArgumentParser(prog='modify-phpipam',
                                     description='Modify phpipam based on defined json/csv config')

    login = parser.add_argument_group("Login",
                                      description="Method to provide login information via args")
    login.add_argument('-u', '--user', dest='username', type=ascii)
    login.add_argument('-p', '--pass', dest='password', type=ascii)
    parser.add_argument('filename', help="Filename for Json work file")

    args = parser.parse_args()

    PHPIpamModifier(args)
