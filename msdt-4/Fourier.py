import os
import sys

import numpy as np


# ������ ����������� ������ ��� ������ � osc
module_path = os.path.abspath("./")
sys.path.append(module_path)
try:
    import Aegis_osc
except ImportError as e:
    raise "�� ������� ������������� ������ ��� ������ � ���������������!"


class Fourier:
    @staticmethod
    def __find_closest_power(self, number):
        """
        ������� ��������� ������� ������ ��� ��������� �����.

        ���������:
        number - ����� �����

        ����������:
        power - ��������� ������� ������ (� ���� ������ �����)
        """
        power = 0
        number -= 1
        while number > 0:
            number >>= 1
            power += 1
        return power

    @staticmethod
    def fill_dataset_for_nulls(signal: list, target_len: int) -> list:
        """�����, ����������� ���� � ����� �������� �� ����������� �����"""
        if len(signal) >= target_len:
            return signal[:target_len]

        fill_len = target_len - len(signal)
        signal.extend([0 for _ in range(fill_len)])
        return signal
    
    @staticmethod
    def four2(signal: list | np.ndarray, d: int = -1) -> list:
        """
        ���������� ��������� ��� �� Python �� ������ ���� �� ����� �.�. ���������.

        ���������:
        x - ������ ������� ������ (������������ �����)
        D - ����������� �������������� (-1 ��� ������� ���, 1 ��� ��������� ���)
        """
        m = 1
        val = 1
        while val < len(signal):
            val <<= 1
            m += 1
        if len(signal) < 2**m:
            signal = Fourier.fill_dataset_for_nulls(signal, 2**m)
        n = 1 << m  # N = 2^M
        y = np.zeros(n)  # ������ ��� ������ �����

        # ������ ��� �������� ���
        for l in range(1, m + 1):
            e = 1 << (m + 1 - l)
            f = e >> 1
            u = 1.0
            v = 0.0

            z = np.pi / f
            c = np.cos(z)
            s = d * np.sin(z)

            for j in range(1, f + 1):
                for i in range(j, n + 1, e):
                    o = i + f - 1
                    p = signal[i - 1] + signal[o]
                    q = y[i - 1] + y[o]  # ������ �����
                    r = signal[i - 1] - signal[o]
                    t = y[i - 1] - y[o]  # ������ �����
                    signal[o] = r * u - t * v
                    y[o] = t * u + r * v
                    signal[i - 1] = p
                    y[i - 1] = q

                w = u * c - v * s
                v = v * c + u * s
                u = w

        # ������������ ��������� (������� ��������)
        j = 1
        for i in range(1, n):
            if i < j:
                j1 = j - 1
                i1 = i - 1
                # ����� ������������ � ������ ������
                signal[j1], signal[i1] = signal[i1], signal[j1]
                y[j1], y[i1] = y[i1], y[j1]
            k = n >> 1
            while k < j:
                j -= k
                k >>= 1
            j += k

        # ������ ��� �������� ���
        if d < 0:  # ������ ���
            for k in range(n):
                a = np.sqrt(signal[k] ** 2 + y[k] ** 2)
                signal[k] = a * 2.0 / n
        else:  # �������� ���
            for k in range(n):
                signal[k] /= n
                y[k] /= n

        signal[0] = 0
        return signal

    @staticmethod
    def abs_values_of_spectr(self, file_osc: Aegis_osc.File_osc, num_osc: int) -> tuple[list, list]:
        buf_size_max = max(2048, (1 << (self.__find_closest_power(file_osc.m_oscDefMod[num_osc].buf_size_max - 1))))
        spectr_buf_size = 1 << (self.__find_closest_power(file_osc.m_oscDefMod[num_osc].buf_size) - 1)
        # interval = file_osc.m_oscDefMod[num_osc].freq / 25 * buf_size_max / spectr_buf_size

        osc = file_osc.getDotOSC(6)
        length_osc = len(osc)
        M = self.__find_closest_power(length_osc)
        osc.extend([0 for _ in range((2 << M - 1) - length_osc)])

        # ���������� ������� ���
        spectra = self.four2(osc.copy(), M, D=-1)
        spectra[0] = 0

        K_mkV = file_osc.m_oscDefMod[num_osc].K_mkV
        freq = file_osc.m_oscDefMod[num_osc].freq
        x = []
        y = []
        for i in range(spectr_buf_size):
            # x.append(round(i * interval))
            x.append(i / (spectr_buf_size / 500))
            y.append(round(spectra[i] * K_mkV / freq * 2896309))
        return x, y