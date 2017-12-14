import pickle

shared = {
"Foo":"Bar", 
"Parrot":"Dead",
"inFileDB" : '/users/heegeradmin/internal/babysleepDatabase/babysleep.db', #database location
"outFile" : '/users/heegeradmin/Sites/sites/dashboard/assets/data/' #location of output files
}

fp = open("shared.pkl","w")
pickle.dump(shared, fp)



# import pickle

# fp = open("shared.pkl")
# shared = pickle.load(fp)
# print shared["Foo"]