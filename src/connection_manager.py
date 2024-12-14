import os
from dotenv import load_dotenv
from src.connections.openai_connection import OpenAIConnection
from src.connections.twitter_connection import TwitterConnection

class ConnectionManager:
    def __init__(self):
        self.connections = {
            'twitter': TwitterConnection(),
            'openai': OpenAIConnection(),
        }

        # Define action parameter requirements
        self.action_params = {
            "get-latest-tweets": {"required": ["username", "count"], "usage": "<username> <count>"},
            "post-tweet": {"required": ["message"], "usage": '"<message>"'},
            "like-tweet": {"required": ["tweet_id"], "usage": "<tweet_id>"},
            "reply-to-tweet": {"required": ["tweet_id", "message"], "usage": '<tweet_id> "<message>"'},
            "generate-text": {"required": ["prompt", "system_prompt", "model"], "usage": '"<prompt>" "<system_prompt>" <model>'},
            "check-model": {"required": ["model"], "usage": "<model>"},
            "list-models": {"required": [], "usage": ""}
        }

    def configure_connection(self, connection_string: str):
        try:
            connection = self.connections[connection_string]
            connection.configure()
            if connection.is_configured():
                print(f"\n✅ SUCCESSFULLY CONFIGURED CONNECTION: {connection_string}")
            else:
                print(f"\n❌ ERROR CONFIGURING CONNECTION: {connection_string}")
        except KeyError:
            print("\nUnknown connection. Try 'list-connections' to see all supported connections.")
        except Exception as e:
            print(f"\nAn error occurred: {e}")

    def check_connection(self, connection_string: str, verbose: bool = False)-> bool:
        try:
            connection = self.connections[connection_string]
            if connection.is_configured():
                if verbose:
                    print(f"\n✅ SUCCESSFULLY CHECKED CONNECTION: {connection_string}")
                return True
            if verbose:
                print(f"\n❌ ERROR CHECKING CONNECTION: {connection_string}")
            return False
        except KeyError:
            print("\nUnknown connection. Try 'list-connections' to see all supported connections.")
            return False
        except Exception as e:
            print(f"\nAn error occurred: {e}")
            return False

    def list_connections(self):
        print("\nAVAILABLE CONNECTIONS:")
        for connection_key, connection in self.connections.items():
            if connection.is_configured():
                print(f"- {connection_key} : ✅ Configured")
            else:
                print(f"- {connection_key} : ❌ Not Configured")

    def list_actions(self, connection_string: str):
        try:
            connection = self.connections[connection_string]
            if connection.is_configured():
                print(f"\n✅ {connection_string} is configured. You can use any of its actions.")
            else:
                print(f"\n❌ {connection_string} is not configured. You must configure a connection in order to use its actions.")
            print("\nAVAILABLE ACTIONS:")
            for action, details in connection.actions.items():
                print(f"- {action}: {details}")
        except KeyError:
            print("\nUnknown connection. Try 'list-connections' to see all supported connections.")
        except Exception as e:
            print(f"\nAn error occurred: {e}")

    def _extract_quoted_text(self, args: list, start_index: int) -> tuple[str, int]:
        if not args[start_index].startswith('"'):
            raise ValueError(f"Text parameter must start with a quote")

        # Handle single argument case
        if args[start_index].endswith('"') and len(args[start_index]) > 1:
            return args[start_index][1:-1], start_index + 1

        # Multiple arguments case
        text_parts = []
        i = start_index
        found_end_quote = False

        while i < len(args):
            part = args[i]
            if i == start_index:
                if len(part) <= 1:  # Just a quote
                    text_parts.append("")
                else:
                    text_parts.append(part[1:])  # Remove starting quote
            elif part.endswith('"'):
                found_end_quote = True
                text_parts.append(part[:-1])  # Remove ending quote
                break
            else:
                text_parts.append(part)
            i += 1

        if not found_end_quote:
            raise ValueError("No closing quote found for text parameter")

        return " ".join(text_parts), i + 1

    def find_and_perform_action(self, action_string: str, connection_string: str, **kwargs):
        try:
            connection = self.connections[connection_string]
            action_info = connection.actions.get(action_string)
            if not action_info:
                raise KeyError(f"Unknown action: {action_string}")

            if 'input_list' in kwargs:
                args = kwargs.pop('input_list')[3:]  # Skip command, connection, and action
                param_info = self.action_params.get(action_string, {})
                required = param_info.get("required", [])
                
                if len(args) < len(required):
                    print(f"\nError: {action_string} requires {len(required)} arguments")
                    print(f"Usage: agent_action {connection_string} {action_string} {param_info.get('usage', '')}")
                    return None

                # Process arguments
                current_arg_index = 0
                for param in required:
                    try:
                        if param in ["message", "prompt", "system_prompt"]:
                            # Extract quoted text
                            text, current_arg_index = self._extract_quoted_text(args, current_arg_index)
                            kwargs[param] = text
                        elif param == "count":
                            kwargs[param] = int(args[current_arg_index])
                            current_arg_index += 1
                        else:
                            kwargs[param] = args[current_arg_index]
                            current_arg_index += 1
                    except (ValueError, IndexError) as e:
                        print(f"\nError processing {param}: {str(e)}")
                        print(f"Usage: agent_action {connection_string} {action_string} {param_info.get('usage', '')}")
                        return None

            return connection.perform_action(action_string, **kwargs)
            
        except KeyError as e:
            print(f"\nUnknown connection or action: {str(e)}")
            return None
        except ValueError as e:
            print(f"\nInvalid argument: {str(e)}")
            return None
        except Exception as e:
            print(f"\nAn error occurred: {e}")
            return None