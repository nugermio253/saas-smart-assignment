from app.statistics import Statistics

s = Statistics()

print("Total:", s.total_assignments())
print("Hoje:", s.assignments_today())

print("\nÚltimas atribuições")
for r in s.last_assignments():
    print(dict(r))

print("\nRanking")
for r in s.tickets_per_agent():
    print(dict(r))
