import pickle

shared = {
"Foo":"Bar", 
"Parrot":"Dead",
}

fp = open("shared.pkl","w")
pickle.dump(shared, fp)



# import pickle

# fp = open("shared.pkl")
# shared = pickle.load(fp)
# print shared["Foo"]