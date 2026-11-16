"""自編例子的計算。Wiki 與簡報上所有自編例子的數字都必須來自這支腳本的輸出。

執行：python scripts/examples.py
輸出：runs/examples.json（給檢查腳本核對）與 runs/examples.txt（給人看）
"""
from __future__ import annotations

import itertools
import json
from fractions import Fraction

from common import RUNS

OUT: dict = {}
TXT: list[str] = []


def say(*parts):
    TXT.append(" ".join(str(p) for p in parts))


# ---------------------------------------------------------------- 共用小工具
def min_v0(seq):
    """給定順序 [(名稱, α, β)]，回傳讓該順序可行的最小初始資源量。"""
    level, need = 0, 0
    for _, a, b in seq:
        need = max(need, a - level)
        level += b - a
    return need


def johnson(jobs):
    """Johnson's rule（Form 2）。jobs: [(名稱, p, q)]。"""
    first = sorted([j for j in jobs if j[1] <= j[2]], key=lambda j: j[1])
    last = sorted([j for j in jobs if j[1] > j[2]], key=lambda j: -j[2])
    return first + last


def flowshop(seq):
    """兩機流程工廠：回傳 (makespan, M2 總閒置時間, M1 區段, M2 區段)。"""
    t1 = t2 = idle = 0
    m1, m2 = [], []
    for name, p, q in seq:
        s1, t1 = t1, t1 + p
        s2 = max(t1, t2)
        idle += s2 - t2
        t2 = s2 + q
        m1.append({"job": name, "start": s1, "end": t1})
        m2.append({"job": name, "start": s2, "end": t2})
    return t2, idle, m1, m2


def composite(seq):
    """Composite job 的 (p*, q*)，依 EJOR2009 §2 的遞迴定義。"""
    _, p, q = seq[0]
    for _, pk, qk in seq[1:]:
        p, q = p + max(0, pk - q), max(0, q - pk) + qk
    return p, q


# ---------------------------------------------------------------- E1 單一工作隊
def e1():
    jobs = [("A", 3, 5), ("B", 6, 2), ("C", 2, 4), ("D", 5, 4)]
    best = johnson(jobs)
    order = "→".join(j[0] for j in best)
    v_best = min_v0(best)
    table = {"".join(j[0] for j in perm): min_v0(perm) for perm in itertools.permutations(jobs)}
    v_opt, v_worst = min(table.values()), max(table.values())
    worst_orders = sorted(k for k, v in table.items() if v == v_worst)
    alpha_order = sorted(jobs, key=lambda j: j[0])
    v_alpha = min_v0(alpha_order)
    assert v_best == v_opt, "Johnson 順序應該達到最小初始資源量"
    cmax, idle, m1, m2 = flowshop(best)
    assert idle == v_best, "M2 閒置時間應等於最小初始資源量"
    cmax_a, idle_a, m1a, m2a = flowshop(alpha_order)
    assert idle_a == v_alpha
    p_star, q_star = composite(best)
    assert p_star == idle
    sum_q = sum(j[2] for j in jobs)
    assert cmax == sum_q + idle and cmax_a == sum_q + idle_a, "makespan 應等於 M2 加工時間總和加上閒置時間"

    levels = []
    level = v_best
    for name, a, b in best:
        levels.append({"job": name, "alpha": a, "beta": b, "before": level, "during": level - a, "after": level - a + b})
        level += b - a
    say("E1 四棟建物 (α,β)：", jobs)
    say("  Johnson 順序：", order, " 最小 v0 =", v_best, "（窮舉 24 種順序的最小值 =", v_opt, "，最大值 =", v_worst, worst_orders, "）")
    say("  依 A→B→C→D：最小 v0 =", v_alpha)
    say("  當作流程工廠 (p=α, q=β)：Johnson 順序 Cmax =", cmax, " M2 閒置 =", idle, "；A→B→C→D Cmax =", cmax_a, " M2 閒置 =", idle_a)
    say("  Johnson 順序的 composite job：p* =", p_star, " q* =", q_star, "；M2 加工時間總和 =", sum_q)
    say("  水位：", levels)
    OUT["E1"] = {
        "desc": "單一工作隊的 relocation problem：四棟建物，求最小初始資源量；同一組數字當作兩機流程工廠",
        "jobs": jobs, "johnson_order": order, "v0_min": v_best, "v0_abcd": v_alpha, "v0_worst": v_worst,
        "cmax_johnson": cmax, "idle_johnson": idle, "cmax_abcd": cmax_a, "idle_abcd": idle_a,
        "composite": [p_star, q_star], "sum_q": sum_q,
        "keys": [order, str(v_best)],
        "blocks": {
            "E1-levels": {"example": "E1-levels", "v0": v_best, "steps": levels,
                          "caption": f"依 {order} 的順序，初始資源 {v_best} 就夠用"},
            "E1-flowshop": {"example": "E1-flowshop",
                            "rows": [{"label": "M1", "bars": m1}, {"label": "M2", "bars": m2}],
                            "caption": f"Johnson 順序 {order}：makespan {cmax}，M2 閒置共 {idle}"},
            "E1-flowshop-abcd": {"example": "E1-flowshop-abcd",
                                 "rows": [{"label": "M1", "bars": m1a}, {"label": "M2", "bars": m2a}],
                                 "caption": f"順序 A→B→C→D：makespan {cmax_a}，M2 閒置共 {idle_a}"},
        },
    }


# ---------------------------------------------------------------- E2 JOSH2010 原文例子
def algorithm_w(jobs, v0):
    """Algorithm W（JOSH2010 §3）。jobs: {名稱: (α, β, w)}，全部 p=1 且 α≤β。"""
    pi1 = sorted(jobs, key=lambda k: -jobs[k][2])                 # 權重由大到小（同分依輸入順序）
    pi2 = sorted(jobs, key=lambda k: -(jobs[k][1] - jobs[k][0]))  # 貢獻由大到小
    v, seq, trace = v0, [], []
    use_pi1 = True
    while len(seq) < len(jobs):
        lst = pi1 if use_pi1 else pi2
        pick = next((k for k in lst if k not in seq and jobs[k][0] <= v), None)
        if pick is None:
            return None, trace
        seq.append(pick)
        trace.append({"pos": len(seq), "list": "π1" if use_pi1 else "π2", "job": pick, "before": v, "after": v + jobs[pick][1] - jobs[pick][0]})
        v += jobs[pick][1] - jobs[pick][0]
        use_pi1 = not use_pi1
    return seq, trace


def weighted_completion(seq, jobs):
    return sum((pos + 1) * jobs[k][2] for pos, k in enumerate(seq))


def feasible(seq, jobs, v0):
    v = v0
    for k in seq:
        if jobs[k][0] > v:
            return False
        v += jobs[k][1] - jobs[k][0]
    return True


def brute_opt(jobs, v0):
    best = None
    for perm in itertools.permutations(jobs):
        if feasible(perm, jobs, v0):
            z = weighted_completion(perm, jobs)
            if best is None or z < best[0]:
                best = (z, perm)
    return best


def e2():
    jobs = {"J1": (0, 2, 1), "J2": (0, 3, 1), "J3": (0, 5, 1), "J4": (10, 10, 5)}
    wspt = sorted(jobs, key=lambda k: -jobs[k][2])
    wspt_ok = feasible(wspt, jobs, 0)
    z_opt, opt = brute_opt(jobs, 0)
    z_free = weighted_completion(wspt, jobs)
    seq, trace = algorithm_w(jobs, 0)
    z_w = weighted_completion(seq, jobs)
    say("E2 JOSH2010 原文的 4 個工作 (α,β,w)，v0=0：", jobs)
    say("  WSPT 順序", wspt, "可行嗎？", wspt_ok, "（若不管資源，Σ w C =", z_free, "）")
    say("  窮舉最佳：", opt, " Σ w C =", z_opt)
    say("  Algorithm W：", seq, " Σ w C =", z_w, trace)
    OUT["E2"] = {
        "desc": "JOSH2010 原文的 4 個工作；WSPT 不可行，Algorithm W 的逐步執行為本腳本計算",
        "wspt_feasible": wspt_ok, "z_without_resource": z_free, "opt": list(opt), "z_opt": z_opt,
        "w_seq": seq, "z_w": z_w, "trace": trace,
        "keys": [str(z_opt), "→".join(seq)],
    }


# ---------------------------------------------------------------- E3 Algorithm W 的緊例
def e3():
    rows = []
    for n in (4, 6, 8, 100):
        half = n // 2
        jobs = {f"J{i}": (0, 0, 1) for i in range(1, half + 1)}
        jobs.update({f"J{i}": (0, 1, 0) for i in range(half + 1, n + 1)})
        seq, _ = algorithm_w(jobs, 0)
        z_w = weighted_completion(seq, jobs)
        z_opt = weighted_completion(list(jobs), jobs)          # 先做完所有有權重的工作
        if n <= 8:
            assert z_opt == brute_opt(jobs, 0)[0]
        rows.append({"n": n, "z_w": z_w, "z_opt": z_opt, "ratio": round(z_w / z_opt, 3),
                     "n2_over_4": n * n // 4, "printed_formula": (n * n - n) / 4, "opt_formula": (n * n + 2 * n) // 8})
        say(f"E3 n={n}: Algorithm W = {z_w}，最佳 = {z_opt}，比值 = {z_w / z_opt:.3f}；n²/4 = {n * n // 4}，原文印的 (n²−n)/4 = {(n * n - n) / 4}")
    OUT["E3"] = {"desc": "JOSH2010 緊例族的實際計算，用來核對原文的封閉式", "rows": rows,
                 "keys": [str(rows[1]["z_w"]), str(rows[1]["z_opt"])]}


# ---------------------------------------------------------------- E4 多個工作隊（單位工時）
def slot_feasible(slots, jobs, v0, m):
    v = v0
    for slot in slots:
        if len(slot) > m or sum(jobs[k][0] for k in slot) > v:
            return False
        v += sum(jobs[k][1] - jobs[k][0] for k in slot)
    return True


def min_makespan(jobs, v0, m):
    """窮舉：把工作分到時段，回傳 (最短時段數, 一個最佳解)。"""
    names = list(jobs)
    for length in range(1, len(names) + 1):
        for assign in itertools.product(range(length), repeat=len(names)):
            if len(set(assign)) != length:
                continue
            slots = [[n for n, a in zip(names, assign) if a == t] for t in range(length)]
            if slot_feasible(slots, jobs, v0, m):
                return length, slots
    return None, None


def greedy_relaxed(jobs, v0):
    """Greedy Algorithm 1（DO2006 §5）：允許把工作切成片段，每個時段解一次 fractional knapsack。"""
    remain = {k: Fraction(1) for k in jobs}
    v, slots = Fraction(v0), []
    while any(r > 0 for r in remain.values()):
        avail = [k for k in jobs if remain[k] > 0 and jobs[k][0] <= v]
        if not avail:
            return None
        avail.sort(key=lambda k: (-(Fraction(jobs[k][1], jobs[k][0]) if jobs[k][0] else Fraction(10**9)), k))
        cap, slot = v, {}
        for k in avail:
            a = jobs[k][0]
            y = remain[k] if a == 0 else min(remain[k], cap / a)
            if y > 0:
                slot[k] = y
                cap -= a * y
        if not slot:
            return None
        for k, y in slot.items():
            remain[k] -= y
            v += (jobs[k][1] - jobs[k][0]) * y
        slots.append(slot)
    return slots


def rounding(frac_slots):
    """Rounding Algorithm（DO2006 §5，全部 δ≥0 的情形）：被切開的工作，在它第一個片段所在時段之後插入新時段整個排入。"""
    slots = [dict(s) for s in frac_slots]
    fragmented = []
    for s in slots:
        for k, y in s.items():
            if y < 1 and k not in fragmented:
                fragmented.append(k)
    result = [[k for k, y in s.items() if k not in fragmented] for s in slots]
    first = {k: next(i for i, s in enumerate(slots) if k in s) for k in fragmented}
    out = []
    for i, base in enumerate(result):
        out.append(base)
        for k in fragmented:
            if first[k] == i:
                out.append([k])
    return [s for s in out if s], fragmented


def splitting(slots, m):
    out = []
    for s in slots:
        for i in range(0, len(s), m):
            out.append(s[i:i + m])
    return out


def e4():
    jobs = {"A": (2, 3), "B": (2, 3), "C": (3, 4), "D": (4, 6), "E": (5, 6), "F": (6, 8)}
    v0 = 4
    one, s1 = min_makespan(jobs, v0, 1)
    two, s2 = min_makespan(jobs, v0, 2)
    unb, s3 = min_makespan(jobs, v0, len(jobs))
    frac = greedy_relaxed(jobs, v0)
    rounded, fragmented = rounding(frac)
    assert slot_feasible(rounded, jobs, v0, len(jobs)), "rounding 後應可行"
    split2 = splitting(rounded, 2)
    assert slot_feasible(split2, jobs, v0, 2), "splitting 後應可行"
    frac_txt = [{k: str(y) for k, y in s.items()} for s in frac]
    say("E4 六個單位工時的工作 (α,β)，v0 =", v0, ":", jobs)
    say("  1 個工作隊：", one, s1, "；2 個工作隊：", two, s2, "；不限工作隊：", unb, s3)
    say("  Greedy Algorithm 1（可切片段）：", len(frac), "個時段", frac_txt)
    say("  Rounding：被切開的工作", fragmented, "→", len(rounded), "個時段", rounded)
    say("  Splitting (m=2)：", len(split2), "個時段", split2)

    def bars(slots):
        rows = {}
        for t, slot in enumerate(slots):
            for lane, k in enumerate(slot):
                rows.setdefault(lane, []).append({"job": k, "start": t, "end": t + 1})
        return [{"label": f"隊 {lane + 1}", "bars": rows[lane]} for lane in sorted(rows)]

    OUT["E4"] = {
        "desc": "多個工作隊、單位工時：資源限制讓多一個工作隊也無法把工期減半",
        "jobs": jobs, "v0": v0, "opt_m1": one, "opt_m2": two, "opt_unbounded": unb,
        "relaxed_len": len(frac), "relaxed": frac_txt, "fragmented": fragmented,
        "rounded_len": len(rounded), "rounded": rounded, "split2_len": len(split2), "split2": split2,
        "keys": [str(two), str(len(rounded))],
        "blocks": {
            "E4-opt-m2": {"example": "E4-opt-m2", "rows": bars(s2), "caption": f"2 個工作隊的最佳排程：{two} 個時段"},
            "E4-rounded": {"example": "E4-rounded", "rows": bars(rounded), "caption": f"Rounding 的結果（不限工作隊數）：{len(rounded)} 個時段"},
            "E4-split2": {"example": "E4-split2", "rows": bars(split2), "caption": f"Splitting 成 2 個工作隊：{len(split2)} 個時段"},
        },
    }


# ---------------------------------------------------------------- E5 固定順序、兩台專用機
def e5():
    # (名稱, p, α, β)
    m1 = [("a1", 2, 2, 3), ("a2", 3, 3, 3), ("a3", 2, 4, 6)]
    m2 = [("b1", 3, 2, 4), ("b2", 2, 5, 5), ("b3", 1, 1, 2)]
    v0 = 4
    horizon = sum(j[1] for j in m1 + m2)

    best = {}

    def search(i, j, t1, t2, events, starts):
        """i, j：兩台機器下一個要排的工作；t1, t2：機器空出的時間；events：(時間, 資源變化)。"""
        if i == len(m1) and j == len(m2):
            comp = {n: s + p for (n, p, _, _), s in zip(m1 + m2, [starts[x[0]] for x in m1 + m2])}
            cmax, total = max(comp.values()), sum(comp.values())
            for key, val in (("cmax", cmax), ("sumc", total)):
                if key not in best or val < best[key][0]:
                    best[key] = (val, dict(starts))
            return
        cands = sorted({0, t1, t2} | {t for t, _ in events})
        for machine in (0, 1):
            if machine == 0 and i == len(m1) or machine == 1 and j == len(m2):
                continue
            name, p, a, b = (m1[i] if machine == 0 else m2[j])
            free = t1 if machine == 0 else t2
            last_start = max(starts.values(), default=0)
            for t in cands:
                if t < free or t < last_start or t > horizon:
                    continue
                level = v0 + sum(d for when, d in events if when <= t)
                if level < a:
                    continue
                # 不能讓之後才歸還的資源被提前借用：檢查 t 之後水位不為負
                new_events = events + [(t, -a), (t + p, b)]
                times = sorted({when for when, _ in new_events})
                if any(v0 + sum(d for when, d in new_events if when <= x) < 0 for x in times):
                    continue
                starts[name] = t
                if machine == 0:
                    search(i + 1, j, t + p, t2, new_events, starts)
                else:
                    search(i, j + 1, t1, t + p, new_events, starts)
                del starts[name]

    search(0, 0, 0, 0, [], {})
    cmax, st = best["cmax"]
    sumc, st2 = best["sumc"]
    naive = sum(j[1] for j in m1), sum(j[1] for j in m2)
    sumc_cmax = max(st2[n] + p for n, p, _, _ in m1 + m2)

    def rows(starts):
        return [{"label": "M1", "bars": [{"job": n, "start": starts[n], "end": starts[n] + p} for n, p, _, _ in m1]},
                {"label": "M2", "bars": [{"job": n, "start": starts[n], "end": starts[n] + p} for n, p, _, _ in m2]}]

    # 最小總完工時間排程的資源水位變化：每個時間點先歸還、再取用（JOSH2016 §2 的事件順序）
    info = {n: (p, a, b) for n, p, a, b in m1 + m2}
    trace, level = [], v0
    for t in sorted({st2[n] for n in info} | {st2[n] + info[n][0] for n in info}):
        done = [n for n in info if st2[n] + info[n][0] == t]
        begin = [n for n in info if st2[n] == t]
        level += sum(info[n][2] for n in done)
        after_return = level
        level -= sum(info[n][1] for n in begin)
        assert level >= 0
        waiting = [n for seq in (m1, m2) for n, *_ in seq if st2[n] > t][:0]
        trace.append({"t": t, "done": done, "start": begin, "after_return": after_return, "after_start": level})
    say("E5 兩台專用機、順序固定，v0 =", v0, " M1:", m1, " M2:", m2)
    say("  最小總完工時間排程的水位：", trace)
    say("  不管資源時兩台機器各自連續加工：", naive, "→ makespan", max(naive))
    say("  最小 makespan =", cmax, st)
    say("  最小總完工時間 =", sumc, st2)
    OUT["E5"] = {
        "desc": "兩台專用機、加工順序固定：只剩「何時開始」要決定，資源仍會逼機器等待",
        "m1": m1, "m2": m2, "v0": v0, "no_resource_makespan": max(naive),
        "cmax": cmax, "cmax_starts": st, "sumc": sumc, "sumc_starts": st2, "sumc_cmax": sumc_cmax, "sumc_trace": trace,
        "keys": [str(cmax), str(max(naive))],
        "blocks": {
            "E5-cmax": {"example": "E5-cmax", "rows": rows(st), "caption": f"最小 makespan = {cmax}（不管資源的話是 {max(naive)}）"},
            "E5-sumc": {"example": "E5-sumc", "rows": rows(st2), "caption": f"最小總完工時間 = {sumc}，這個排程的 makespan 是 {sumc_cmax}"},
        },
    }


# ---------------------------------------------------------------- E6 雙代理人
def e6():
    # (名稱, 代理人, p, d)
    jobs = [("a1", 1, 3, 6), ("a2", 1, 2, 9), ("a3", 1, 5, 12), ("b1", 2, 4, 6), ("b2", 2, 3, 16)]
    theta = Fraction(1, 2)

    def evaluate(seq):
        t, obj, ok, comp = 0, Fraction(0), True, {}
        for name, ag, p, d in seq:
            t += p
            comp[name] = t
            if ag == 1:
                obj += theta * max(0, t - d) + (1 - theta) * t
            elif t > d:
                ok = False
        return ok, obj, comp

    results = [(evaluate(perm), perm) for perm in itertools.permutations(jobs)]
    feas = [(obj, perm, comp) for (ok, obj, comp), perm in results if ok]
    obj_opt, opt, comp_opt = min(feas, key=lambda x: x[0])
    spt = sorted(jobs, key=lambda j: j[2])
    ok_spt, obj_spt, _ = evaluate(spt)
    init = sorted([j for j in jobs if j[1] == 2], key=lambda j: j[3]) + sorted([j for j in jobs if j[1] == 1], key=lambda j: j[2])
    ok_init, obj_init, _ = evaluate(init)
    name = lambda seq: "→".join(j[0] for j in seq)
    by = {j[0]: j for j in jobs}
    spt_b1 = evaluate(spt)[2]["b1"]                      # 純 SPT 時 b1 的完工時間
    prefix_b1 = by["a1"][2] + by["a3"][2] + by["b1"][2]   # 先排 a1、a3 之後，b1 最早的完工時間
    assert prefix_b1 > by["b1"][3]
    say("E6 雙代理人 5 個工作 (名稱, 代理人, p, d)，θ = 1/2：", jobs)
    say("  全部 120 種順序中可行（AG2 不延遲）的有", len(feas), "種")
    say("  純 SPT：", name(spt), "可行？", ok_spt, " 目標值", float(obj_spt), "；b1 完工時間", spt_b1, "（交期", by["b1"][3], "）")
    say("  若前兩個位置排 a1、a3，b1 最早在", prefix_b1, "完成 → 依 Property 2 剪枝")
    say("  SA 初始解（AG2 依 EDD、再 AG1 依 SPT）：", name(init), "可行？", ok_init, " 目標值", float(obj_init))
    say("  最佳：", name(opt), " 目標值", float(obj_opt), comp_opt)
    OUT["E6"] = {
        "desc": "雙代理人單機排程的小例子：AG1 最小化 θΣT+(1−θ)ΣC，AG2 不得延遲",
        "jobs": jobs, "theta": "1/2", "n_perm": len(results), "n_feasible": len(feas),
        "spt": name(spt), "spt_feasible": ok_spt, "spt_obj": float(obj_spt), "spt_b1_completion": spt_b1, "prefix_a1_a3_b1_completion": prefix_b1,
        "init": name(init), "init_feasible": ok_init, "init_obj": float(obj_init),
        "opt": name(opt), "opt_obj": float(obj_opt),
        "keys": [name(opt), f"{float(obj_opt):g}"],
        "blocks": {
            "E6-opt": {"example": "E6-opt", "rows": [{"label": "機器", "bars": [
                {"job": n, "start": comp_opt[n] - p, "end": comp_opt[n], "group": ag} for n, ag, p, d in opt]}],
                "caption": f"最佳順序 {name(opt)}：目標值 {float(obj_opt):g}"},
        },
    }


if __name__ == "__main__":
    for fn in (e1, e2, e3, e4, e5, e6):
        fn()
    RUNS.mkdir(exist_ok=True)
    (RUNS / "examples.json").write_text(json.dumps(OUT, ensure_ascii=False, indent=1), encoding="utf-8")
    (RUNS / "examples.txt").write_text("\n".join(TXT) + "\n", encoding="utf-8")
    import sys
    sys.stdout.reconfigure(encoding="utf-8")
    print("\n".join(TXT))
