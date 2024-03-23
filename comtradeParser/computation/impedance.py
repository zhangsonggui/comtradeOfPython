import numpy as np


def compute_line_impedance(this_before_v_xfl: list, this_before_i_xfl: list,
                           this_after_v_xfl: list, this_after_i_xfl: list,
                           other_before_v_xfl: list, other_after_v_xfl: list):
    # 正序阻抗=（本侧故障前正序电压x对侧故障后负序电压-对侧故障前正序电压x本侧故障后负序电压）/
    #         （本侧故障前正序电流x对侧故障后负序电压-对侧故障前电压x本侧故障后负序电流）
    """
    通过本侧故障前后电压、电流通道和对侧故障前后电压，计算线路正序阻抗
    :param this_before_v_xfl: 本侧故障前电压序分量数据
    :param this_before_i_xfl: 本侧故障前电流序分量数据
    :param this_after_v_xfl: 本侧故障后电压序分量数据
    :param this_after_i_xfl: 本侧故障后电流序分量数据
    :param other_before_v_xfl: 对侧故障前电压序分量数据
    :param other_after_v_xfl: 对本侧故障后电压序分量数据
    :return: 
    """
    order_impedance = ((this_before_v_xfl[1] * other_after_v_xfl[2] - other_before_v_xfl[1] *
                        this_after_v_xfl[2]) /
                       (this_before_i_xfl[1] * other_after_v_xfl[2] - other_before_v_xfl[1] *
                        this_after_i_xfl[2]))
    return np.around(order_impedance, 3)


def compute_impedance(this_u, other_u, i):
    """
    通过两侧电压和本侧电流相量计算阻抗
    @param this_u: 本侧站电压相量
    @param other_u: 对侧站电压相量
    @param i: 电流相量
    @return: 返回计算的线路阻抗值
    """
    _impedance = 0
    if i != 0:
        _impedance = (this_u - other_u) / i
    return np.around(_impedance, 3)

