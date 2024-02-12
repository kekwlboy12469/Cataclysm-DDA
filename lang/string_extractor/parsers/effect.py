from .condition import parse_condition
from ..write_text import write_text
from ..write_text import write_translation_or_var


def parse_effect(effects, origin, comment=""):
    if not type(effects) is list:
        effects = [effects]
    for eff in effects:
        if type(eff) is dict:
            if not comment:
                if "id" in eff:
                    comment = "effect \"{}\"".format(eff["id"])
                elif "effect_id" in eff:
                    comment = "effect \"{}\"".format(eff["effect_id"])
                else:
                    comment = "an effect"
            if "message_npc" in eff:
                write_text(eff["message_npc"], origin,
                           comment="NPC message in {}".format(comment))
            if "u_buy_monster" in eff and "name" in eff:
                write_text(eff["name"], origin,
                           comment="Nickname for creature '{}' in {}".
                           format(eff["u_buy_monster"], comment))
            if "snippet" not in eff or eff["snippet"] is False:
                if "message" in eff:
                    write_translation_or_var(eff["message"], origin,
                                             comment="Message in {}"
                                             .format(comment))
                if "u_message" in eff:
                    write_translation_or_var(eff["u_message"], origin,
                                             comment="Player message in {}"
                                             .format(comment))
                if "npc_message" in eff:
                    write_translation_or_var(eff["npc_message"], origin,
                                             comment="NPC message in {}"
                                             .format(comment))
                if "u_make_sound" in eff and type(eff["u_make_sound"]) is str:
                    write_text(eff["u_make_sound"], origin,
                               comment="Player makes sound in {}".
                               format(comment))
                if "npc_make_sound" in eff and \
                        type(eff["npc_make_sound"]) is str:
                    write_text(eff["npc_make_sound"], origin,
                               comment="NPC makes sound in {}".format(comment))
            if "set_string_var" in eff and "i18n" in eff and eff["i18n"] is True:
                str_vals = eff["set_string_var"]
                if type(str_vals) is not list:
                    str_vals = [str_vals]
                for val in str_vals:
                    write_translation_or_var(val, origin,
                                             comment="Text variable value in {}"
                                             .format(comment))
            if "spawn_message" in eff:
                write_text(eff["spawn_message"], origin,
                           comment="Player sees monster spawns in {}"
                           .format(comment))
            if "spawn_message_plural" in eff:
                write_text(eff["spawn_message_plural"], origin,
                           comment="Player sees monsters spawn in {}"
                           .format(comment))
            if "u_teleport" in eff or "npc_teleport" in eff:
                if "success_message" in eff:
                    write_text(eff["success_message"], origin,
                               comment="Success message in teleportation in {}"
                               .format(comment))
                if "fail_message" in eff:
                    write_text(eff["fail_message"], origin,
                               comment="Fail message in teleportation in {}"
                               .format(comment))
            if "variables" in eff:
                parse_effect_variables(eff["variables"], origin, comment)
            if "run_eocs" in eff:
                if type(eff["run_eocs"]) is list:
                    for eoc in eff["run_eocs"]:
                        if type(eoc) is dict:
                            parse_effect_on_condition(eoc, origin,
                                                      comment="nested EOCs in {}"
                                                      .format(comment))
            if "run_eoc_selector" in eff:
                for name in eff.get("names", []):
                    write_translation_or_var(name, origin,
                                             comment="EOC option name in {}"
                                             .format(comment))
                for desc in eff.get("descriptions", []):
                    write_translation_or_var(desc, origin,
                                             comment="EOC option description "
                                             "in {}".format(comment))
                if "title" in eff:
                    write_text(eff["title"], origin,
                               comment="EOC selection title in {}"
                               .format(comment))
            if "weighted_list_eocs" in eff:
                for e in eff["weighted_list_eocs"]:
                    if type(e[0]) is dict:
                        if "effect" in e[0]:
                            parse_effect(e[0]["effect"], origin,
                                         comment="nested effect in {}"
                                         .format(comment))
            if "switch" in eff:
                for e in eff["cases"]:
                    parse_effect(e["effect"], origin,
                                 comment="nested effect in switch statement in {}"
                                 .format(comment))
            if "place_override" in eff:
                write_translation_or_var(eff["place_override"], origin,
                                         comment="place name in {}"
                                         .format(comment))


def parse_effect_on_condition(json, origin, comment=""):
    id = json["id"]
    if "effect" in json:
        if comment:
            parse_effect(json["effect"], origin,
                         comment="effect in EoC \"{}\" in {}"
                         .format(id, comment))
        else:
            parse_effect(json["effect"], origin,
                         comment="effect in EoC \"{}\"".format(id))
    if "false_effect" in json:
        if comment:
            parse_effect(json["false_effect"], origin,
                         comment="false effect in EoC \"{}\" in {}"
                         .format(id, comment))
        else:
            parse_effect(json["false_effect"], origin,
                         comment="false effect in EoC \"{}\"".format(id))
    if "condition" in json:
        parse_condition(json["condition"], origin)


def parse_effect_variables(json, origin, comment):
    if "message_success" in json:
        write_text(json["message_success"], origin,
                   comment="Success message casting spell \"{}\" in {}"
                   .format(json["spell_to_cast"], comment))
    if "message_fail" in json:
        write_text(json["message_fail"], origin,
                   comment="Fail message casting spell \"{}\" in {}"
                   .format(json["spell_to_cast"], comment))
    if "success_message" in json:
        write_text(json["success_message"], origin,
                   comment="Success message in {}".format(comment))
    if "failure_message" in json:
        write_text(json["failure_message"], origin,
                   comment="Failure message in {}".format(comment))
