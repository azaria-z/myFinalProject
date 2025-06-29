from air_conditioner import Air_Conditioner

# אני מנסה לבדוק שכל הפונקציות במזגן פועלות

ac=Air_Conditioner()
# print(ac.get_name())
# print(ac.get_state_mode())
# print(ac.change_mode("cool"))
# print(ac.get_state_mode())
# print(ac.change_mode("heat"))
# print(ac.get_state_mode())
# print(ac.change_mode("fan"))
# print(ac.get_state_mode())
# print(ac.change_mode("dry"))
# print(ac.get_state_mode())
# print(ac.change_mode("sleep"))
# print(ac.get_state_mode())
# print(ac.change_mode("cool"))
# print(ac.get_state_mode())
# print(ac.change_temperature(3, True))
# print(ac.get_action_status("temperature"))
# print(ac.get_state_mode())

# print(ac.change_blinds_position("vertical swing"))
print(ac.get_action_status("temperature"))
print(ac.get_action_status("mode"))
print(ac.get_action_status("fan speed"))
print(ac.get_action_status("blinds"))
print(ac.get_action_status("display"))
print(ac.get_action_status("angle"))
print(ac.get_action_status("state"))
print(ac.get_action_status("name"))

