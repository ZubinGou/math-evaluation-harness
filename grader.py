"""
This logic is largely copied from the Hendrycks' MATH release (math_equivalence), and borrowed from:
- https://github.com/microsoft/ProphetNet/tree/master/CRITIC
- https://github.com/openai/prm800k
"""
import re
import multiprocessing
from math import isclose
from typing import Union

from sympy import simplify, N
from sympy.parsing.sympy_parser import parse_expr
from sympy.parsing.latex import parse_latex
from latex2sympy2 import latex2sympy



def is_digit(s):
    try:
        float(str(s).replace(",", ""))
        return True
    except ValueError:
        return False

def str_to_pmatrix(input_str):  
    input_str = input_str.strip()  
    matrix_str = re.findall(r'\{.*,.*\}', input_str)  
    pmatrix_list = []  
  
    for m in matrix_str:  
        m = m.strip('{}')
        pmatrix = r'\begin{pmatrix}' + m.replace(',', '\\') + r'\end{pmatrix}'  
        pmatrix_list.append(pmatrix)  
  
    return ', '.join(pmatrix_list)


def math_equal(prediction: Union[bool, float, str],
                reference: Union[float, str],
                include_percentage: bool = True,
                is_close: bool = True,
                timeout: bool = False,
                ) -> bool:
    """
    Exact match of math if and only if:
    1. numerical equal: both can convert to float and are equal
    2. symbolic equal: both can convert to sympy expression and are equal
    """
    try: # 1. numerical equal
        if is_digit(prediction) and is_digit(reference):
            prediction = float(str(prediction).replace(",", ""))
            reference = float(str(reference).replace(",", ""))
            # number questions
            if include_percentage:
                gt_result = [reference / 100, reference, reference * 100]
            else:
                gt_result = [reference]
            for item in gt_result:
                try:
                    if is_close:
                        if numeric_equal(prediction, item):
                            return True
                    else:
                        if item == prediction:
                            return True
                except Exception:
                    continue
            return False
    except:
        pass

    if not prediction and prediction not in [0, False]:
        return False

    # 2. symbolic equal
    reference = str(reference).strip()
    prediction = str(prediction).strip()

    ## pmatrix (amps)
    if "pmatrix" in prediction and not 'pmatrix' in reference:
        reference = str_to_pmatrix(reference)

    ## deal with [], (), {}
    pred_str, ref_str = prediction, reference
    if (prediction.startswith("[") and prediction.endswith("]") and not reference.startswith("(")) or \
        (prediction.startswith("(") and prediction.endswith(")") and not reference.startswith("[")):
        pred_str = pred_str.strip("[]()")
        ref_str = ref_str.strip("[]()")
    for s in ['{', "}", "(", ")"]:
        ref_str = ref_str.replace(s, "")
        pred_str = pred_str.replace(s, "")
    if pred_str.lower() == ref_str.lower():
        return True

    ## [a, b] vs. [c, d], return a==c and b==d
    if (prediction.startswith("[") and prediction.endswith("]")) and (reference.startswith("[") and reference.endswith("]")) or \
        (prediction.startswith("(") and prediction.endswith(")")) and (reference.startswith("(") and reference.endswith(")")):
        pred_parts = prediction[1:-1].split(",")
        ref_parts = reference[1:-1].split(",")
        if len(pred_parts) == len(ref_parts):
            if all([math_equal(pred_parts[i], ref_parts[i], include_percentage, is_close) for i in range(len(pred_parts))]):
                return True

    # symbolic equal with sympy
    if timeout:
        if call_with_timeout(symbolic_equal_process, prediction, reference):
            return True
    else:
        if symbolic_equal(prediction, reference):
            return True

    return False


def math_equal_process(param):
    return math_equal(param[-2], param[-1])


def numeric_equal(prediction: float, reference: float):
    # Note that relative tolerance has significant impact 
    # on the result of the synthesized GSM-Hard dataset
    if reference.is_integer():
        return isclose(reference, round(prediction), abs_tol=1e-4)
    else:
        # round prediction to refence precision
        prediction = round(prediction, len(str(reference).split(".")[-1]))
        return isclose(reference, prediction, rel_tol=1e-6)


def symbolic_equal(a, b):
    def _parse(s):
        for f in [parse_latex, parse_expr, latex2sympy]:
            try:
                return f(s)
            except:
                pass
        return s
    a = _parse(a)
    b = _parse(b)

    # direct equal
    try:
        if str(a) == str(b) or a == b:
            return True
    except:
        pass

    # simplify equal
    try:
        if a.equals(b) or simplify(a-b) == 0:
            return True
    except:
        pass

    # equation equal
    try:
        if (abs(a.lhs - a.rhs)).equals(abs(b.lhs - b.rhs)):
            return True
    except:
        pass

    try:
        if numeric_equal(float(N(a)), float(N(b))):
            return True
    except:
       pass

    # matrix
    try:
        # if a and b are matrix
        if a.shape == b.shape:
            _a = a.applyfunc(lambda x: round(x, 3))
            _b = b.applyfunc(lambda x: round(x, 3))
            if _a.equals(_b):
                return True
    except:
        pass

    return False


def symbolic_equal_process(a, b, output_queue):  
    result = symbolic_equal(a, b)
    output_queue.put(result)  


def call_with_timeout(func, *args, timeout=1, **kwargs):  
    output_queue = multiprocessing.Queue()  
    process_args = args + (output_queue,)  
    process = multiprocessing.Process(target=func, args=process_args, kwargs=kwargs)  
    process.start()  
    process.join(timeout)  
  
    if process.is_alive():  
        process.terminate()  
        process.join()  
        return False  
  
    return output_queue.get()


def _test_math_equal():
    # print(math_equal("0.0833333333333333", "\\frac{1}{12}"))
    # print(math_equal("(1,4.5)", "(1,\\frac{9}{2})"))
    # print(math_equal("\\frac{x}{7}+\\frac{2}{7}", "\\frac{x+2}{7}", timeout=True))
    # print(math_equal("\\sec^2(y)", "\\tan^2(y)+1", timeout=True))
    # print(math_equal("\\begin{pmatrix}-\\frac{7}{4}&-2\\\\4&\\frac{1}{4}\\end{pmatrix}", "(\\begin{pmatrix}-\\frac{7}{4}&-2\\\\4&\\frac{1}{4}\\\\\\end{pmatrix})", timeout=True))

    # pred = '\\begin{pmatrix}\\frac{1}{3x^{2/3}}&0&0\\\\0&1&0\\\\-\\sin(x)&0&0\\end{pmatrix}'
    # gt = '(\\begin{pmatrix}\\frac{1}{3\\sqrt[3]{x}^2}&0&0\\\\0&1&0\\\\-\\sin(x)&0&0\\\\\\end{pmatrix})'

    # pred= '-\\frac{8x^2}{9(x^2-2)^{5/3}}+\\frac{2}{3(x^2-2)^{2/3}}'
    # gt= '-\\frac{2(x^2+6)}{9(x^2-2)\\sqrt[3]{x^2-2}^2}'

    # pred =  '-34x-45y+20z-100=0'
    # gt = '34x+45y-20z+100=0'

    # pred = '\\frac{100}{3}'
    # gt = '33.3'

    # pred = '\\begin{pmatrix}0.290243531202435\\\\0.196008371385084\\\\-0.186381278538813\\end{pmatrix}'
    # gt = '(\\begin{pmatrix}0.29\\\\0.196\\\\-0.186\\\\\\end{pmatrix})'

    pred = '\\frac{\\sqrt{\\sqrt{11}+\\sqrt{194}}}{2\\sqrt{33}+15}'
    gt = '\\frac{\\sqrt{\\sqrt{11}+\\sqrt{194}}}{15+2\\sqrt{33}}'

    print(math_equal(pred, gt, timeout=True))


if __name__ == "__main__":
    _test_math_equal()


