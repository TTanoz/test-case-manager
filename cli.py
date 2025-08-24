from storage import load_from_file, save_to_file
from domain import (
    add_suite, list_suites, suite_details,
    add_case, search_cases, list_cases, connect_case_to_suite
)
from runs import create_run, add_run_result, run_summary
from reports import report_by_tag, report_flaky_candidates

def safe_int_input(prompt):
    while True:
        s = input(prompt)
        try:
            return int(s)
        except ValueError:
            print("Invalid number, try again.")

def cli():
    data = load_from_file()
    while True:
        print("""
1 List suites
2 Add suite
3 Suite details
4 Add case
5 Search cases
6 List cases (filtered)
7 Connect case to suite
8 Create run
9 Add result to run
10 Run summary
11 Report: By tag
12 Report: Flaky candidates
13 Exit
""")
        choice = safe_int_input("> ")

        if choice == 1:
            suites = list_suites(data)
            if not suites:
                print("No Suites")
                continue
            for sid, name, count in suites:
                print(f"{sid} - {name} (Cases: {count})")

        elif choice == 2:
            name = input("Suite name: ").strip()
            desc = input("Description: ").strip()
            sid = add_suite(data, name, desc, auto_save=True)
            print(f"✅ Suite added (id={sid})")

        elif choice == 3:
            sid = safe_int_input("Suite id: ")
            det = suite_details(data, sid)
            if not det:
                print("No match")
                continue
            print(f"{det['id']} - {det['name']} | {det['description']}")
            if not det["cases"]:
                print("No cases in this suite.")
            else:
                for c in det["cases"]:
                    print(f" - {c['id']} {c['title']} [{c['status']}]")

        elif choice == 4:
            title = input("Case title: ").strip()
            priority = input("Priority (P1/P2/P3): ").strip()
            tags = [t.strip() for t in input("Tags (csv): ").split(",") if t.strip()]
            n = safe_int_input("Steps count: ")
            steps = []
            for i in range(1, n + 1):
                act = input(f"{i}. action: ")
                exp = input(f"{i}. expected: ")
                steps.append({"no": i, "action": act, "expected": exp})
            cid = add_case(data, title, priority, tags, steps, auto_save=True)
            print(f"✅ Case added (id={cid})")

        elif choice == 5:
            q = input("Search (title/tags): ")
            found = search_cases(data, q)
            if not found:
                print("There is no case")
            else:
                for c in found:
                    print(f"{c.get('id')}. {c.get('title')} [{c.get('status')}]")

        elif choice == 6:
            f_status = input("Status (empty to skip): ").strip() or None
            f_priority = input("Priority (empty to skip): ").strip() or None
            f_tag = input("Tag (empty to skip): ").strip() or None
            f_q = input("Title contains (empty to skip): ").strip() or None
            filters = {}
            if f_status: filters["status"] = f_status
            if f_priority: filters["priority"] = f_priority
            if f_tag: filters["tag"] = f_tag
            if f_q: filters["q"] = f_q
            result = list_cases(data, filters)
            if not result:
                print("No cases found")
            else:
                print("ID  | Title                       | Status   | Pri | Tags")
                print("----+-----------------------------+----------+-----+----------------")
                for c in result:
                    print(f"{str(c.get('id')).ljust(3)} | "
                          f"{str(c.get('title')).ljust(27)} | "
                          f"{str(c.get('status')).ljust(8)} | "
                          f"{str(c.get('priority')).ljust(3)} | "
                          f"{', '.join(c.get('tags', []))}")

        elif choice == 7:
            cid = safe_int_input("Case id: ")
            sid = safe_int_input("Suite id: ")
            try:
                changed = connect_case_to_suite(data, cid, sid, auto_save=True)
                print("✅ Connected." if changed else "Already connected.")
            except ValueError as e:
                print(str(e))

        elif choice == 8:
            sid = safe_int_input("Suite id: ")
            try:
                rid = create_run(data, sid, auto_save=True)
                print(f"✅ Run created: {rid}")
            except ValueError as e:
                print(str(e))

        elif choice == 9:
            rid = safe_int_input("Run id: ")
            cid = safe_int_input("Case id: ")
            result = input("Result (pass/fail/blocked/skip): ").strip()
            notes = input("Notes (optional): ")
            try:
                add_run_result(data, rid, cid, result, notes, auto_save=True)
                print("✅ Result added/updated.")
            except ValueError as e:
                print(str(e))

        elif choice == 10:
            rid = safe_int_input("Run id: ")
            try:
                summary = run_summary(data, rid)
                c = summary["counts"]
                print(f"--- Run {rid} Summary ---")
                print(f"Time: {summary['executed_at']} | Suite: {summary['suite_id']} | Total: {summary['total']}")
                print(f"PASSED : {c['pass']}")
                print(f"FAILED : {c['fail']}")
                print(f"BLOCKED: {c['blocked']}")
                print(f"SKIP   : {c['skip']}")
            except ValueError as e:
                print(str(e))

        elif choice == 11:
            tag = input("Tag: ")
            rows = report_by_tag(data, tag)
            if not rows:
                print("No cases for this tag.")
            else:
                for r in rows:
                    print(f"{r['id']} | {r['title']} | last={r['last_result']}")

        elif choice == 12:
            n = safe_int_input("How many recent runs? (default 5): ")
            if n <= 0: n = 5
            rows = report_flaky_candidates(data, last_n_runs=n)
            if not rows:
                print("No flaky candidates.")
            else:
                for r in rows:
                    print(f"{r['case_id']} | {r['title']} | seen={','.join(r['seen'])}")

        elif choice == 13:
            print("Bye")
            break

        else:
            print("Invalid choice.")

if __name__ == "__main__":
    cli()