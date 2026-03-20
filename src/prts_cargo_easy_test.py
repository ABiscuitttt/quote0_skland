import prts_api as prts

print(prts.cargo_tables())
print(prts.cargo_fields("chara"))
print(len(prts.cargo_query("tables=chara&fields=cn,charId,nation")))
