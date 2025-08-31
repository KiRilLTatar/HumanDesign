from django.shortcuts import render
from django.views.decorators.http import require_POST
from django.http import JsonResponse
import sxtwl
from datetime import datetime
import pytz
import re
from .utils.required_const import SEASON_TABLE, ELEMENT_TABLE, HIDDEN_STEMS_TABLE, SUPPORTING_ELEMENTS, SEASON_BOOST, DEITY_TABLE, STAR_TABLE, CZY_CZY_TABLE, JIE_QI_TABLE_1985
from .utils.pillar import Pillar
import logging

logger = logging.getLogger(__name__)

@require_POST
def calc_of_the_badza_card(request):
    name = request.POST.get("name", "").strip()
    birth_date = request.POST.get("birthDate", "").strip()
    birth_time = request.POST.get("birthTime", "").strip()
    birth_place = request.POST.get("birthPlace", "").strip()
    gender = request.POST.get("gender", "").strip()
    question = request.POST.get("question", "").strip()

    errors = {}

    if not name:
        errors["name"] = "Введите, пожалуйста, имя пользователя"
    
    if not birth_date:
        errors["birthDate"] = "Введите, пожалуйста, дату рождения"
    else:
        try:
            birth_datetime = datetime.strptime(birth_date, "%Y-%m-%d")
            if birth_datetime.year < 1900 or birth_datetime.year > datetime.now().year:
                errors["birthDate"] = "Дата рождения должна быть между 1900 и текущим годом"
        except ValueError:
            errors["birthDate"] = "Неверный формат даты (ожидается YYYY-MM-DD)"

    if not birth_time:
        errors["birthTime"] = "Введите, пожалуйста, время рождения"
    else:
        if not re.match(r"^\d{2}:\d{2}$", birth_time):
            errors["birthTime"] = "Неверный формат времени (ожидается HH:MM)"
        else:
            try:
                datetime.strptime(birth_time, "%H:%M")
            except ValueError:
                errors["birthTime"] = "Некорректное время рождения"

    if not birth_place:
        errors["birthPlace"] = "Введите, пожалуйста, место рождения"
    
    if not gender:
        errors["gender"] = "Выберите, пожалуйста, пол"
    elif gender not in ["male", "female"]:
        errors["gender"] = "Некорректное значение пола (male или female)"

    if errors:
        return JsonResponse({"status": "error", "errors": errors}, status=400)

    try:
        pillar = Pillar(birth_date, birth_time, birth_place)
        print(pillar.birth_datetime_china)
    except Exception as e:
        return JsonResponse({"status": "error", "errors": {"birthDateTime": f"Ошибка обработки даты/времени: {str(e)}"}}, status=400)
    
    try: 
        all_pillar = pillar.get_bazi()

        pers_element = all_pillar["day_pillar"].stem

        hidden_stems = {
            "year": get_hidden_stems(all_pillar["year_pillar"].branch),
            "month": get_hidden_stems(all_pillar["month_pillar"].branch),
            "day": get_hidden_stems(all_pillar["day_pillar"].branch),
            "hour": get_hidden_stems(all_pillar["hour_pillar"].branch),
        }

        season = get_season(all_pillar["month_pillar"].branch)
        strength = calculate_chart_strength(pers_element, hidden_stems, season, all_pillar)

        deities = calculate_deities(
            pers_element,
            [all_pillar["year_pillar"].stem, all_pillar["month_pillar"].stem, all_pillar["day_pillar"].stem, all_pillar["hour_pillar"].stem],
            hidden_stems
        )

        stars = calculate_stars(all_pillar["day_pillar"], all_pillar["year_pillar"])

        luck_pillars = calculate_luck_pillars(all_pillar["year_pillar"], gender, birth_datetime)

        result = {
            "name": name,
            "birthDate": birth_date,
            "birthTime": birth_time,
            "birthPlace": birth_place,
            "gender": gender,
            "question": question,
            "bazi_card": {
                "year_pillar": {"stem": all_pillar["year_pillar"].stem, "branch": all_pillar["year_pillar"].branch},
                "month_pillar": {"stem": all_pillar["month_pillar"].stem, "branch": all_pillar["month_pillar"].branch},
                "day_pillar": {"stem": all_pillar["day_pillar"].stem, "branch": all_pillar["day_pillar"].branch},
                "hour_pillar": {"stem": all_pillar["hour_pillar"].stem, "branch": all_pillar["hour_pillar"].branch},
                "personality_element": pers_element,
                "hidden_stems": hidden_stems,
                "strength": strength,
                "deities": deities,
                "stars": stars,
                "luck_pillars": luck_pillars,
            }
        }

        return JsonResponse({"status": "success", "data": result})

    except Exception as e:
        return JsonResponse({"status": "error", "errors": {"calculation": f"Ошибка расчета карты: {str(e)}"}}, status=500)

def get_hidden_stems(branch):
    """
    parametrs: земная ветвь (str)

    return->Список скрытых Небесных Стволов или пустой список (list)

    Возвращает скрытые Небесные Стволы для Земной Ветви
    """
    return HIDDEN_STEMS_TABLE.get(branch, [])

def get_season(branch):
    """
    parametrs: земная ветвь месяца (str)
    
    return->сезон (str)

    Возвращает сезон по Земной ветви месяца
    """
    
    return SEASON_TABLE.get(branch, "Неизвестно")

def calculate_chart_strength(pers_element, hidden_stems, season, all_pillar):
    """
    patametrs:
        pers_element (str): небесный ствол дня
        hidden_stems (dict): сткрытые небесные стволы
        season (str): сезон рождения
        all_pillar (dict): по солнечному календарю год, месяц, день, час
    
    return->сила карты (str)

    Расчитывает силу карты Ба цзы
    """

    pers_element_type = ELEMENT_TABLE.get(pers_element, "").split()[0]

    element_count  = {"Дерево": 0, "Огонь": 0, "Земля": 0, "Металл": 0, "Вода": 0}
    for stems in hidden_stems.values():
        for stem in stems:
            element = ELEMENT_TABLE.get(stem, "").split()[0]
            if element in element_count:
                element_count[element] += 1

    for stem in [all_pillar["year_pillar"].stem, all_pillar["month_pillar"].stem, all_pillar["day_pillar"].stem, all_pillar["hour_pillar"].stem]:
        element = ELEMENT_TABLE.get(stem, "").split()[0]
        if element in element_count:
            element_count[element] += 1

    sup_count = sum(element_count[el] for el in SUPPORTING_ELEMENTS[pers_element_type])

    season_element = SEASON_BOOST.get(season, "Земля")
    season_mod = 2 if season_element == pers_element_type else -1 if season_element in ["Дерево", "Огонь", "Металл", "Вода"] else 0

    total_sup = sup_count + season_mod
    if total_sup > 5:
        return "Сильная"
    elif total_sup < 3:
        return "Слабая"
    return "Сбалансированная"

def calculate_deities(pers_element, stems, hidden_stems):
    """
    patametrs:
        pers_element (str): небесный ствол дня
        stems (list): список Небесных Стволов четырех столпов
        hidden_stems (dict): сткрытые небесные стволы
    
    return->словарь с божествами для каждого ствола (dict)

    Расчитывает 10 божест для каждого ствола и скрытого ствола
    """
    pers_element_type = ELEMENT_TABLE.get(pers_element, "").split()[0]
    deities = {
        "year_stem": None,
        "month_stem": None,
        "day_stem": None,
        "hidden_stems": {"year": [], "month": [], "day": [], "hour": []}
    }

    for i, stem in enumerate(stems):
        stem_type = ELEMENT_TABLE.get(stem, "").split()[0]
        is_yin = "Инь" in ELEMENT_TABLE.get(stem, "")
        deity = DEITY_TABLE.get(pers_element_type, {}).get(stem_type, ["Неизвестно"])[1 if is_yin else 0]
        deities[["year_stem", "month_stem", "day_stem", "hour_stem"][i]] = deity

    for pillar in ["year", "month", "day", "hour"]:
        deities["hidden_stems"][pillar] = []
        for stem in hidden_stems[pillar]:
            stem_type = ELEMENT_TABLE.get(stem, "").split()[0]
            is_yin = "Инь" in ELEMENT_TABLE.get(stem, "")
            deity = DEITY_TABLE.get(pers_element_type, {}).get(stem_type, ["Неизвестно"])[1 if is_yin else 0]
            deities["hidden_stems"][pillar].append(deity)

    return deities 

def calculate_stars(day_pillar, year_pillar):
    """
    patametrs:
        day_pillar (object): столп дня
        year_pillar (object): столп года
    
    return->список найденных звезд (list)

    Рассчитывает Символические звезды.
    """

    stars = []
    day_stem, day_branch = day_pillar.stem, day_pillar.branch
    year_branch = year_pillar.branch

    if day_branch in STAR_TABLE["Благородный человек"].get(day_stem, []):
        stars.append("Благородный человек")

    if year_branch in STAR_TABLE["Цветок Персика"].get(day_branch, []):
        stars.append("Цветок Персика")

    return stars 

def calculate_luck_pillars(year_pillar, gender, birth_datetime):
    """
    patametrs:
        year_pillar (object): столп года
        gender (str): пол
        birth_datetime (datetime): дата и время рождения
    
    return-> dict: Словарь с полями:
              - luck_pillars: Список словарей [{"start_age": float, "pillar": str}, ...]
              - active_pillar: Текущий активный столп или None
              - errors: Список ошибок (если есть)

    Рассчитывает Столпы Удачи.
    """

    errors = []

    if not hasattr(year_pillar, 'stem') or not hasattr(year_pillar, 'branch'):
        errors.append("Некорректный формат year_pillar")
        return {"luck_pillars": [], "active_pillar": None, "errors": errors}
    if gender not in ["male", "female"]:
        errors.append("Некорректный пол: должен быть 'male' или 'female'")
        return {"luck_pillars": [], "active_pillar": None, "errors": errors}
    if not isinstance(birth_datetime, datetime):
        errors.append("Некорректный формат birth_datetime")
        return {"luck_pillars": [], "active_pillar": None, "errors": errors}

    
    yang_stems = ["Цзя", "Бин", "У", "Гэн", "Жэнь"]
    is_yang = year_pillar.stem in yang_stems
    is_forward = (gender == "male" and is_yang) or (gender == "female" and not is_yang)

    
    current_pillar = f"{year_pillar.stem} {year_pillar.branch}"
    try:
        current_index = CZY_CZY_TABLE.index(current_pillar)
    except ValueError:
        errors.append(f"Столп {current_pillar} не найден в таблице Цзя Цзы")
        return {"luck_pillars": [], "active_pillar": None, "errors": errors}

    
    birth_year = birth_datetime.year
    birth_date = birth_datetime.date()
    min_days = float('inf')

    for jie_qi, date_info in JIE_QI_TABLE_1985.items():
        try:
            jq_date = datetime(birth_year, date_info["month"], date_info["day"]).date()
            days_diff = (jq_date - birth_date).days
            if is_forward:
                if days_diff >= 0 and days_diff < min_days:
                    min_days = days_diff
            else:
                if days_diff <= 0 and abs(days_diff) < min_days:
                    min_days = abs(days_diff)
        except ValueError:
            logger.warning(f"Некорректная дата Цзе Ци для {jie_qi}: {date_info}")
            continue

    if min_days == float('inf'):
        logger.warning("Цзе Ци не найден, используется start_age=5")
        start_age = 5
        errors.append("Цзе Ци не найден, использован запасной start_age=5")
    else:
        start_age = round(min_days / 3.0, 1)

    luck_pillars = []
    for i in range(10):
        pillar_index = (current_index + (i if is_forward else -i)) % 60
        luck_pillars.append({
            "start_age": round(start_age + i * 10, 1),
            "pillar": CZY_CZY_TABLE[pillar_index]
        })

    current_year = datetime.now().year
    current_age = current_year - birth_year
    active_pillar = None
    for pillar in luck_pillars:
        if pillar["start_age"] <= current_age < pillar["start_age"] + 10:
            active_pillar = {
                "pillar": pillar["pillar"],
                "start_age": pillar["start_age"],
                "end_age": pillar["start_age"] + 10
            }
            break

    return {
        "luck_pillars": luck_pillars,
        "active_pillar": active_pillar,
        "errors": errors
    }

@require_POST
def decryption_card(request):
    pass