#!/usr/bin/env python3
"""
quizhash.py — считает хэши ответов для блоков самопроверки (quiz.js).

Нормализация и число повторов хэша ДОЛЖНЫ совпадать с quiz.js.
Так в HTML попадает только хэш — сам ответ из страницы не виден и не перебирается.

Использование:
    # один вопрос с несколькими допустимыми ответами:
    python3 tools/quizhash.py basics2-led "резистор" "через резистор"

    # вывод сразу для вставки в data-hash (через пробел):
    #   <div class="quiz-q" data-id="basics2-led" data-hash="ХЭШ1 ХЭШ2">

Параметр --iter должен совпадать с data-iter у блока .quiz (по умолчанию 2000).
"""
import argparse
import hashlib
import re

DEFAULT_ITER = 2000


def normalize(s: str) -> str:
    s = (s or "").lower().replace("ё", "е")
    s = s.replace(",", ".")                          # десятичная запятая → точка
    s = re.sub(r"[^0-9a-zа-я .\-]", " ", s)          # лишние символы → пробел
    s = re.sub(r"\s+", " ", s).strip()
    s = re.sub(r"^[.\-]+|[.\-]+$", "", s).strip()    # крайние точки/дефисы
    return s


def quizhash(qid: str, answer: str, iterations: int = DEFAULT_ITER) -> str:
    h = hashlib.sha256((qid + "|" + normalize(answer)).encode("utf-8")).hexdigest()
    for _ in range(iterations - 1):
        h = hashlib.sha256(h.encode("utf-8")).hexdigest()
    return h


def main() -> None:
    p = argparse.ArgumentParser(description="Хэши ответов для quiz.js")
    p.add_argument("id", help="data-id вопроса (соль; делает хэши уникальными)")
    p.add_argument("answers", nargs="+", help="один или несколько допустимых ответов")
    p.add_argument("--iter", type=int, default=DEFAULT_ITER)
    args = p.parse_args()

    hashes = [quizhash(args.id, a, args.iter) for a in args.answers]
    print("id:        ", args.id)
    for a, h in zip(args.answers, hashes):
        print(f'  "{a}"  ->  норм="{normalize(a)}"')
        print("            ", h)
    print()
    print('data-hash="' + " ".join(hashes) + '"')


if __name__ == "__main__":
    main()
