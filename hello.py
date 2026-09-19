import json
from datetime import date
from pathlib import Path


DATA_FILE = Path(__file__).with_name("bills.json")


def load_bills():
	if not DATA_FILE.exists():
		return []
	try:
		return json.loads(DATA_FILE.read_text(encoding="utf-8"))
	except (json.JSONDecodeError, OSError):
		print("Could not read bills.json. Starting with an empty list.")
		return []


def save_bills(bills):
	DATA_FILE.write_text(json.dumps(bills, indent=2), encoding="utf-8")


def money(amount):
	return f"${amount:,.2f}"


def show_summary(bills):
	current_month = date.today().strftime("%Y-%m")
	month_bills = [bill for bill in bills if bill["due_date"].startswith(current_month)]
	total = sum(bill["amount"] for bill in month_bills)
	paid = sum(bill["amount"] for bill in month_bills if bill["paid"])
	remaining = total - paid
	print(f"\nMonthly summary for {current_month}")
	print(f"Total:     {money(total)}")
	print(f"Paid:      {money(paid)}")
	print(f"Remaining: {money(remaining)}")


def list_bills(bills):
	if not bills:
		print("\nNo bills have been added yet.")
		return
	print("\nBills")
	for index, bill in enumerate(sorted(bills, key=lambda item: item["due_date"]), start=1):
		status = "PAID" if bill["paid"] else "DUE"
		print(
			f"{index}. {bill['name']} | {money(bill['amount'])} | "
			f"due {bill['due_date']} | {status}"
		)


def add_bill(bills):
	name = input("Bill name: ").strip()
	if not name:
		print("A bill name is required.")
		return
	try:
		amount = float(input("Amount: $"))
		due_date = input("Due date (YYYY-MM-DD): ").strip()
		date.fromisoformat(due_date)
	except ValueError:
		print("Enter a valid amount and date, such as 2026-09-25.")
		return
	bills.append({"name": name, "amount": amount, "due_date": due_date, "paid": False})
	save_bills(bills)
	print(f"Added {name}.")


def mark_paid(bills):
	list_bills(bills)
	if not bills:
		return
	try:
		selection = int(input("Bill number to mark paid: "))
		bill = sorted(bills, key=lambda item: item["due_date"])[selection - 1]
	except (ValueError, IndexError):
		print("Please choose a listed bill number.")
		return
	bill["paid"] = True
	save_bills(bills)
	print(f"Marked {bill['name']} as paid.")


def main():
	bills = load_bills()
	print("Monthly Bill Tracker")
	while True:
		show_summary(bills)
		print("\n1. List bills\n2. Add bill\n3. Mark bill paid\n4. Exit")
		choice = input("Choose an option: ").strip()
		if choice == "1":
			list_bills(bills)
		elif choice == "2":
			add_bill(bills)
		elif choice == "3":
			mark_paid(bills)
		elif choice == "4":
			print("Goodbye!")
			break
		else:
			print("Choose 1, 2, 3, or 4.")


if __name__ == "__main__":
	main()
