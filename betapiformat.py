from time import sleep, time
import regex as re
import sys, psutil, pymem, subprocess
import numpy as np
from pdmemedit import Pdmemory
from a_pandas_ex_sequence_search import pd_add_find_sequence
import pandas as pd
from exceptdrucker import errwrite
from copy import deepcopy
# from rich import print

rencols = {
    "3P": "PLACE_365",
    "3W": "WIN_365",
    "4Q": "MARKET_GROUP_PAIR_ID",
    "AB": "FINANCIALS_PRICE_1",
    "AC": "STATS_COLUMN",
    "AD": "ADDITIONAL_DATA",
    "AE": "STATS_CELL",
    "AF": "ARCHIVE_FIXTURE_INFO",
    "AH": "ASIAN_HOVER",
    "AI": "ANIMATION_ID",
    "AJ": "FINANCIALS_MARKET_ODDS_2",
    "AM": "ANIMATION_ICON",
    "AO": "ANIMATION_TOPIC",
    "AP": "STATS_PANE",
    "AQ": "FINANCIALS_CLOSE_TIME",
    "AS": "ADDITIONAL_STATS",
    "AT": "ANIMATION_TEXT",
    "AU": "AUDIO_AVAILABLE",
    "AV": "ARCHIVE_VIDEO_AVAILABLE",
    "BB": "BUTTON_BAR",
    "BC": "BOOK_CLOSES",
    "BD": "PULL_BET_DATA",
    "BE": "BET",
    "BH": "BLURB_HEADER",
    "BI": "BUTTON_BAR_INDEX",
    "BL": "BASE_LINE",
    "BO": "BASE_ODDS",
    "BS": "BANNER_STYLE",
    "BT": "INFO_POD_DETAIL_2",
    "C1": "C1_ID",
    "C2": "C2_ID",
    "C3": "MINI_DIARY_C3",
    "CB": "CLOSE_BETS_DISABLED",
    "CC": "BET_TYPE_PULL",
    "CD": "COMPETITION_DROPDOWN",
    "CF": "CONFIG",
    "CG": "GLOBAL_CONFIG",
    "CI": "CLASS_ID",
    "CK": "COMPETITION_KEY",
    "CL": "CLASSIFICATION",
    "CM": "BET_CALL_FEATURE_DISABLED",
    "CN": "CHANNEL",
    "CO": "COLUMN",
    "CP": "CLOSE_BETS_PRESENTATION_PULL_DISABLED",
    "CR": "CLASS_ORDER",
    "CS": "CLASSIFICATIONS",
    "CT": "COMPETITION_NAME",
    "CU": "CURRENT_INFO",
    "D1": "DATA_1",
    "D2": "DATA_2",
    "D3": "DATA_3",
    "D4": "DATA_4",
    "D5": "DATA_5",
    "DA": "DIARY_DAY",
    "DC": "DISPLAY_CLOCK",
    "DD": "DISPLAY_DATE",
    "DE": "DESCRIPTION",
    "DM": "IN_PLAY_LAUNCHER_DISPLAY_MODE",
    "DN": "DIARY_NAME",
    "DO": "DEFAULT_OPEN",
    "DP": "DECIMAL_PLACES",
    "DR": "DIARY_REFRESH",
    "DS": "DISPLAY_SCORE",
    "DX": "DISABLE_COLUMN_DISTRIBUTION",
    "DY": "DIARY",
    "EA": "EVENT_TIME",
    "EC": "ERROR_CODE",
    "ED": "EXTRA_DATA_2",
    "EE": "ETOTE_LINK_DATA",
    "EI": "EVENT_ID",
    "EL": "EXTRA_STATS_AVAILABLE",
    "EM": "EMPTY",
    "EP": "EXTRA_PARTICIPANTS",
    "ER": "ERROR_LOGGING",
    "ES": "EMBEDDED_STREAMING",
    "ET": "END_TIME",
    "EV": "EVENT",
    "EW": "EACH_WAY",
    "EX": "EXTRA_DATA_1",
    "FD": "FORCE_DISPLAY",
    "FF": "FILTERING",
    "FI": "FIXTURE_PARENT_ID",
    "FK": "FINANCIALS_FEED_1",
    "FL": "FINANCIALS_PERIOD_1",
    "FM": "FINANCIALS_MARKET_1A",
    "FN": "FINANCIALS_MARKET_1B",
    "FO": "FINANCIALS_FEED_2",
    "FP": "FINANCIALS_PERIOD_2",
    "FQ": "FINANCIALS_MARKET_2A",
    "FR": "FINANCIALS_MARKET_2B",
    "FS": "FIXTURE_STARTED",
    "FW": "FIXED_WIN",
    "GC": "LOTTO_GAME_CODE",
    "GM": "LOTTO_GAME_MARKET",
    "GR": "GROUP",
    "HA": "HANDICAP",
    "HD": "HANDICAP_FORMATTED",
    "HI": "HEADER_IMAGE",
    "HM": "MARKET_BAR",
    "HO": "DEFAULT_OPEN_HOMEPAGE",
    "HP": "SHOW_ON_HOMEPAGE",
    "HS": "HASH",
    "HT": "POD_HEADER_TEXT",
    "HU": "INFO_BANNER_SUBHEAD2",
    "HV": "POD_BODY_TEXT_2",
    "HW": "HORSE_WEIGHT",
    "HY": "HORSE_AGE",
    "I2": "ID2",
    "IA": "AUDIO_ICON",
    "IB": "IBOX",
    "IC": "ICON",
    "ID": "ID",
    "IF": "IN_PLAY",
    "IG": "IMAGE_ID",
    "IM": "IMAGE",
    "IN": "INFO",
    "IO": "ITEM_ORDER",
    "IP": "IN_PLAY_AVAILABLE_FLAG",
    "IQ": "INFO_POD_IMAGE1",
    "IR": "INRUNNING_INFO",
    "IS": "INFO_POD_IMAGE_PATH1",
    "IT": "TOPIC_ID",
    "ITX": "TOPIC_IDX",
    "IU": "INFO_POD_IMAGE2",
    "JN": "JOCKEY_PULL",
    "JY": "JOCKEY",
    "KC": "KIT_COLORS",
    "KI": "KIT_ID",
    "L1": "BREADCRUMB_LEVEL_1",
    "LA": "LABEL",
    "LB": "INFO_POD_LINK_1_DISPLAY_TEXT",
    "LC": "EVENT_COUNT",
    "LD": "INFO_POD_LINK_1_C1_ID_TABLE",
    "LE": "INFO_POD_LINK_1_C2_ID",
    "LF": "INFO_POD_LINK_1_C2_ID_TABLE",
    "LG": "INFO_POD_LINK_2_ID",
    "LH": "INFO_POD_LINK_2_DISPLAY_TEXT",
    "LI": "INFO_POD_LINK_2_C1_ID",
    "LJ": "INFO_POD_LINK_2_C1_ID_TABLE",
    "LK": "INFO_POD_LINK_2_C2_ID",
    "LL": "INFO_POD_LINK_2_C2_ID_TABLE",
    "LM": "POD_ENCODED_URL_1",
    "LN": "POD_ENCODED_URL_2",
    "LO": "DEFAULT_OPEN_LEFT",
    "LP": "LIVE_IN_PLAY",
    "LQ": "INFO_POD_LINK_1_C3_ID_TABLE",
    "LR": "INFO_POD_LINK_1_C3_SECTION_ID",
    "LS": "PREVIOUS_SET_SCORE",
    "MA": "MARKET",
    "MB": "BET_CALL_V2_DISABLED",
    "MC": "CUSTOMER_TO_CUSTOMER_CALLING_FEATURE_DISABLED",
    "MD": "MATCHLIVE_PERIOD",
    "ME": "MULTI_EVENT",
    "MF": "MATCH_FLAG",
    "MG": "MARKET_GROUP",
    "ML": "MATCH_LENGTH",
    "MM": "MERGE_MARKET",
    "MO": "SECONDARY_UK_EVENT",
    "MP": "MATCH_POSTPONED",
    "MR": "CUSTOMER_TO_REPRESENTATIVE_CALLING_FEATURE_DISABLED",
    "MS": "MEDIA_ID",
    "MT": "BET_CALL_V2_TWILIO_DISABLED",
    "MU": "MULTILINE",
    "MW": "LOTTO_MAX_WINNINGS",
    "MY": "MARKET_STYLE",
    "N2": "NAME2",
    "NA": "NAME",
    "NC": "CLOTH_NUMBER",
    "NG": "NGENERA",
    "NH": "NEXT_HEADER",
    "NM": "NON_MATCH_BASED",
    "NR": "NON_RUNNER",
    "NT": "NEUTRAL_VENUE_TEXT",
    "NV": "NEUTRAL_VENUE",
    "OB": "BANKER_OPTION",
    "OD": "ODDS",
    "OH": "ODDS_HISTORY",
    "OO": "ODDS_OVERRIDE",
    "OP": "OPEN_BETS_PRESENTATION_PULL_DISABLED",
    "OR": "ORDER",
    "OT": "OTHERS_AVAILABLE",
    "PA": "PARTICIPANT",
    "PB": "PUSH_BALANCE_ENABLED",
    "PC": "PAGE_DATA_1",
    "PD": "PAGE_DATA",
    "PE": "PARTICIPANTS_EXCEEDED",
    "PF": "PUSH_FLAG",
    "PG": "PENALTY_GOALS",
    "PH": "PHONE_ONLY",
    "PI": "PLAYING_INDICATOR",
    "PN": "CLOTH_NUMBER_PULL",
    "PO": "POD_STACK_ORDER",
    "PP": "POD_OPEN",
    "PR": "PREFERENCE_ID",
    "PS": "POD_STACK",
    "PT": "PRODUCT_TYPE",
    "PV": "PREMIUM_VERSION",
    "PX": "NO_OFFER",
    "PY": "PARTICIPANT_STYLE",
    "RA": "RANGE",
    "RC": "RESULT_CODE",
    "RD": "RACE_DETAILS",
    "RE": "BET_RETURNS",
    "RG": "REGION",
    "RI": "R4_COMMENT",
    "RO": "DEFAULT_OPEN_RIGHT",
    "RS": "RUNNER_STATUS",
    "RT": "RESULTS_TEXT",
    "S1": "MATCHLIVE_STATS_1",
    "S2": "MATCHLIVE_STATS_2",
    "S3": "MATCHLIVE_STATS_3",
    "S4": "MATCHLIVE_STATS_4",
    "S5": "MATCHLIVE_STATS_5",
    "S6": "MATCHLIVE_STATS_6",
    "S7": "MATCHLIVE_STATS_7",
    "S8": "MATCHLIVE_STATS_8",
    "SA": "CHANGE_STAMP",
    "SB": "SCOREBOARD_TYPE",
    "SC": "SCORE",
    "SD": "AUDIO_ID",
    "SE": "SECONDARY_EVENT",
    "SF": "SPOTLIGHT_FORM",
    "SG": "STAT_GROUP",
    "SI": "IMAGE_ID_PULL",
    "SL": "SCORES_CELL",
    "SM": "START_TIME",
    "SN": "DRAW_NUMBER_PULL",
    "SP": "STAT_PERIOD",
    "SS": "SHORT_SCORE",
    "ST": "INFO_POD_DETAIL_1",
    "SU": "SUCCESS",
    "SV": "MATCHLIVE_AVAILABLE",
    "SY": "STYLE",
    "SZ": "STAT_LOCATION",
    "T1": "C1_TABLE",
    "T2": "C2_TABLE",
    "T3": "MINI_DIARY_T3",
    "T4": "TEXT_4",
    "T5": "TEXT_5",
    "TA": "TIME_ADDED",
    "TB": "BREADCRUMB_TRAIL",
    "TC": "BET_TOTE_TYPE",
    "TD": "COUNTDOWN",
    "TE": "TEAM",
    "TG": "TEAM_GROUP",
    "TI": "TMR_SERVER",
    "TL": "LEAGUE_TOPIC",
    "TM": "STAT_TIME",
    "TN": "TRAINER_NAME",
    "TO": "EMPTY_TOPIC_ID",
    "TP": "TIME_STAMP",
    "TR": "TAX_RATE",
    "TS": "TMR_SECS",
    "TT": "TMR_TICKING",
    "TU": "TMR_UPDATED",
    "TX": "TAX_METHOD",
    "UC": "CURRENT_INFO_V4",
    "UF": "UPDATE_FREQUENCY",
    "VA": "VALUE",
    "VC": "MATCHLIVE_ANIMATION",
    "VD": "VIRTUAL_DATA",
    "VI": "VIDEO_AVAILABLE",
    "VL": "VISIBLE",
    "VR": "VIRTUAL_RACE",
    "VS": "VIDEO_STREAM",
    "WG": "WIZE_GUY",
    "WM": "WINNING_MARGIN",
    "XB": "CHECK_BOX",
    "XC": "EXCLUDE_COLUMN_NUMBERS",
    "XI": "EXTRA_INFO_NODE",
    "XL": "CONTROLLER",
    "XP": "SHORT_POINTS",
    "XT": "EXTRA_TIME_LENGTH",
    "XY": "MATCHLIVE_COORDINATES",
    "ZA": "TIMEZONE_ADJUSTMENT",
    "_V": "PADDOCK_VIDEO_AVAILABLE",
    "UNDEFINED": "EVENT_TYPE",
}


def get_data(limite=5, encodingdata="cp1252"):
    limi = int(limite)
    coux = 0
    stoptrigger = False
    try:
        while not stoptrigger:
            allresults.append([])
            internalid0 = 0

            for la in allmems:
                hlist.clear()
                memmi.clear()
                try:
                    la.update_region_df(
                        limitfunction=lambda x: True,
                        dtypes=(
                            "S1",
                            np.uint8,
                        ),
                        allowed_protections=(
                            pymem.ressources.structure.MEMORY_PROTECTION.PAGE_READWRITE,
                        ),
                    )
                    memmi.append(
                        la.regiondf.loc[
                            (
                                la.regiondf.aa_dump_numpy_uint8.s_find_sequence(
                                    np8stuff,
                                    exception_val=[],
                                    distance=2,
                                ).apply(lambda x: len(x) > 0)
                            )
                        ]
                    )
                    for h in pd.concat(memmi, ignore_index=True).aa_dump_S1.apply(
                        lambda x: b"".join(x).decode(encodingdata, "ignore")
                    ):
                        hlist.append(h)
                    tmptimestamp = time()
                    internalid1 = 0
                    for h in hlist:
                        internalid2 = 0
                        for hh in h.split("|"):
                            linhapronta = hh.strip()
                            if not linhapronta.endswith(";") or not re.search(
                                r"^[A-Z0-9]{2,}", linhapronta
                            ):
                                continue

                            allresults[-1].append(
                                f'{linhapronta.rstrip(";")};TIMESTAMP={tmptimestamp};INTERNALID0={internalid0};INTERNALID1={internalid1};INTERNALID2={internalid2}'
                            )
                            internalid2 += 1
                        internalid1 += 1
                    print("\n-----------------------\n")
                    internalid0 += 1
                except Exception as e:
                    errwrite()
            coux += 1
            if coux > limi:
                stoptrigger = True
                break
    except KeyboardInterrupt:
        try:
            sleep(1)
        except:
            pass
    return None


bravebro = subprocess.Popen(
    [
        r"C:\Program Files\BraveSoftware\Brave-Browser\Application\brave.exe",
        "https://www.bet365.com/#/IP/B1",
    ]
)
pd_add_find_sequence()
allmapped = []
sleep(5)
allpids = []
allprocs = []

for q in psutil.process_iter():
    try:
        if q.name() == "brave.exe":
            allprocs.append(q)
    except Exception:
        pass
resi = []
allmems = []
memmi = []
np8stuff = np.array([79, 68, 61], dtype=np.uint8)
for q in allprocs:
    allmems.append(Pdmemory(pid=q.pid, filename=None))
hlist = []
allresults = []
get_data(limite=5, encodingdata="cp1252")
# from threading import Lock,Thread
# lock=Lock()
# lock.acquire()
# lock.release()

colunas = set()
parsedresults = []
for a in allresults:
    for aa in a:
        parsedresults.append({})
        for ini, aaa in enumerate(aa.split(";")):
            if ini == 0 and "=" not in aaa:
                aaa = "UNDEFINED=" + aaa
            try:
                kcol, vcol = aaa.split("=", maxsplit=1)
                colunas.add(kcol)
                parsedresults[-1][kcol] = vcol
            except Exception:
                errwrite()
parsedresults2 = deepcopy(parsedresults)
for ini, singledict in enumerate(parsedresults):
    for kcol in colunas:
        for col in colunas - set(singledict.keys()):
            parsedresults2[ini][col] = ""

df = pd.DataFrame(parsedresults2)
df.columns = [rencols.get(x, x) for x in df.columns.to_list()]
df.EVENT_TYPE = df.EVENT_TYPE.apply(lambda x: rencols.get(x, x))
df.to_excel("c:\\scrapesamples.xlsx")
