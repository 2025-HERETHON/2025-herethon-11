#컵 사이즈 계산
def calculate_bust_size(bust, underbust):
    bust_diff = bust - underbust

    if bust_diff >= 25:
        cup_size = "H"
    elif bust_diff >= 22.5:
        cup_size = "G"
    elif bust_diff >= 20:
        cup_size = "F"
    elif bust_diff >= 17.5:
        cup_size = "E"
    elif bust_diff >= 15:
        cup_size = "D"
    elif bust_diff >= 12.5:
        cup_size = "C"
    elif bust_diff >= 10:
        cup_size = "B"
    elif bust_diff >= 7.5:
        cup_size = "A"
    else:
        cup_size = "AA"

    return cup_size

#골반 사이즈 계산
def calculate_pelvis_size(waist, hip):
    #1차 계산 : 힙&허리
    if waist <= 60 and 82 <= hip <= 87:
        return "XS(85)"
    elif 60 < waist <= 65 and 87 < hip <= 92:
        return "S(90)"
    elif 65 < waist <= 75 and 92 < hip <= 97:
        return "M(95)"
    elif 75 < waist <= 80 and 97 < hip <= 102:
        return "L(100)"
    elif 80 < waist <= 85 and 102 < hip <= 107:
        return "XL(105)"
    elif 85 < waist <= 90 and 107 < hip <= 112:
        return "XXL(110)"
    elif waist > 90 and 112 < hip <= 117:
        return "3XL(115)"

    #2차 계산 : 1차에서 맞는게 없을 경우, 힙을 기준으로 판단
    if 82 <= hip <= 87:
        return "XS(85)"
    elif 87 < hip <= 92:
        return "S(90)"
    elif 92 < hip <= 97:
        return "M(95)"
    elif 97 < hip <= 102:
        return "L(100)"
    elif 102 < hip <= 107:
        return "XL(105)"
    elif 107 < hip <= 112:
        return "XXL(110)"
    elif 112 < hip <= 117:
        return "3XL(115)"

    #예외 처리: 범위에 해당하지 않는 경우
    return "측정 불가"