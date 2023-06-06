import json
from hikari.utils import handle_error_response


class ActionsHelper:
    def __init__(self, wrapper):
        self.wrapper = wrapper
        self.power = PowerHelper(self)

class PowerHelper:
    def __init__(self, actions_helper):
        self.actions_helper = actions_helper

    def get_power_state(self):
        response = self.actions_helper.wrapper.get(path="redfish/v1/systems/1")

        if response.status_code == 200:
            power_state = response.json().get("PowerState")
            return power_state
        return None

    @property
    def on(self):
        return self.power(state="on")

    @property
    def off(self):
        return self.power(state="off")

    @property
    def status(self):
        return self.get_power_state()

    def power(self, state):
        current_state = self.get_power_state()

        if current_state is None:
            return None

        if current_state == "On":
            if state == current_state.lower():
                return "Server is already powered on"

        if current_state == "Off":
            if state == current_state.lower():
                return "Server is already powered off"

        reset_type = "On" if state == "on" else "PushPowerButton"
        response = self.actions_helper.wrapper.post(
            path = "redfish/v1/systems/1/Actions/ComputerSystem.Reset",
            data = json.dumps({"ResetType": f"{reset_type}"})
        )
        if response.status_code == 200:
            message = f"Initiating power {state}..."
            if state == 'on':
                message += "\nPlease wait a few minutes for the boot sequence to complete."
            return message

        error_message = handle_error_response(response, state)
        return error_message
