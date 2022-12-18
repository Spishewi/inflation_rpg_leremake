# Author : Grégpry Plantard

#from json import dump, load
import pickle
from sys import stderr
from os.path import exists,dirname, sep
from os import makedirs
from glob import glob

class Filable:    
    class Format:
        JSON = ".json"
        PICKLE = ".pickle"
        DEFAULT = PICKLE

    def save(self,file_name = None, file_directory = None, format = Format.DEFAULT, verbose = False):
        """
        Enregistre un objet dans un fichier.
        <file_name> = nom du fichier de sauvegarde
        <format> = type de format utiliser. Utilisez la classe <Savable.Format> pour les choix
        <verbode> == False : affiche du texte de controle à l'enregistrement du fichier.
        """
        if file_name == None:
           file_name = "object_"+str(id(self))+str(format)
        
        # Entregistrement de l'objet en fichier texte
        complet_file_name = file_name
        if file_directory != None:
            complet_file_name = "." + sep + file_directory + sep + complet_file_name
        if dirname(complet_file_name) != "":
            makedirs(dirname(complet_file_name), exist_ok=True)

        if format == Filable.Format.JSON:
            print("Le format JSON n'est pas encore pris en charge", file=stderr)
        else: # Default : Pickle
            # creation des repertoires 
            
            with open(complet_file_name, "wb") as file:
                pickle.dump(self, file)
                if verbose == True:
                    print("Objet enregistré avec succès sous le fichier '"+str(complet_file_name)+"'")
                return complet_file_name

    @staticmethod
    def load(file_name, format = Format.DEFAULT, verbose = False):
        """
        Charge un objet à partir d'un fichier.
        <file_name> = nom du fichier de sauvegarde
        <format> = type de format utiliser. Utilisez la classe <Savable.Format> pour les choix
        <verbode> == False : affiche du texte de controle lors de la lecture du fichier.
        """
        #test si le fichier existe
        if not exists(file_name):
            print(f"Erreur : Le fichier '{file_name}' n'existe pas.", file=stderr)
            #raise NameError()
            return None

        #chargement du fichier
        if format == Filable.Format.JSON:
            print("Le format JSON n'est pas encore pris en charge.", file=stderr)

        elif format == Filable.Format.PICKLE:
            if verbose:
                print("Chargement du fichier '"+str(file_name)+"'")
            with open(file_name, "rb") as file:
                return pickle.load(file)
        
        else:
            print(f"Le format {format} n'est pas encore pris en charge.", file=stderr)

    def massload(file_name_pattern, format = Format.DEFAULT, verbose = False):
        """
        Charge plusieurs objet à partir d'un format de nom (exemple : "object_*.pickle").
        <file_name> = nom du fichier de sauvegarde
        <format> = type de format utiliser. Utilisez la classe <Savable.Format> pour les choix
        <verbode> == False : affiche du texte de controle lors de la lecture du fichier.
        """
        file_name_list = glob(file_name_pattern)
        if verbose:
            if len(file_name_list) <=1 :
                print (len(file_name_list),"fichier à charger")
            else:
                print (len(file_name_list),"fichiers à charger")
        objects = []
        for file_name in file_name_list:
            objects.append(Filable.load(file_name, format, verbose))

        return objects