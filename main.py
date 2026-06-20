from store import Store

new_store = Store()


new_store.set("First",1)
new_store.set("Second",2)

print(new_store.delete("First"))
print(new_store.delete("First"))