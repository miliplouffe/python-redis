package main

import (
	"encoding/json"
	"flag"
	"fmt"
	"html/template"
	_ "image/jpeg"
	"log"
	"net"
	"net/http"
	"os"
	"structure"
	"time"
)

type PageVariables struct {
	Pentree         string
	Parriere        string
	PsousSol        string
	Cprincipale     string
	Csecondaire     string
	DSousSol 		string
	CsousSol        string
	Dsalon          string
	Dbureau         string
	DchauffeEau     string
	DatelierEau     string
	DfumeeBas       string
	DfumeeAtelier   string
}

const (
	serviceSystemeTextIn = "192.168.1.123:9095"
	serviceSystemDataOut = "192.168.1.123:9094"
)

var root = flag.String("root", ".", "file system path")
var detecteur structure.Equipements
var DateHeureThreadConnexion time.Time
var valeurRetour PageVariables
var valeurEnvoyeDebut bool
var ipClient string

//     <ahref="http://admin.lrmm.com/CMS/Media/Preview_2910_70_en-CA_0_Contexte_legal_de_l_acces_a_l_eau_au_Quebec.pdf">Contexte légal de l'accès à l'eau du Québec</a>
//<ahref="https://www.erudit.org/fr/revues/cd1/1970-v11-n1-cd5001975/1004779ar.pdf">Le droit Québécois et l'eau (1663-1969)</a>

func main() {
	valeurEnvoyeDebut = false

	//go threadSysteme()
	DateHeureThreadConnexion = time.Now()

	http.HandleFunc("/", HomePage)
	http.Handle("/images/", http.StripPrefix("/images/", http.FileServer(http.Dir("/home/pi/go/src/images"))))
	http.HandleFunc("/action", action)
	assigneValeurRetour()
	log.Fatal(http.ListenAndServe(":8081", nil))
}

func action(w http.ResponseWriter, r *http.Request) {
	if valeurEnvoyeDebut == false {
		SendToSysteme("1")
		valeurEnvoyeDebut = true
	}

	submit := r.FormValue("submit")
	//fmt.Printf("requete du client pour  serveur       %s \n", submit)

	if submit == "shutdown" {
		SendToSysteme("shutdown")
	}

	if submit == "miseAJour" {
		SendToSysteme("1")
	}

	if submit == "Activation partielle" {
		SendToSysteme("Activation partielle")
	}

	if submit == "Activation complete" {
		SendToSysteme("Activation complete")
	}

	if submit == "Desactivation" {
		SendToSysteme("Desactivation")
	}

	time.Sleep(200 * time.Millisecond)
	assigneValeurRetour()
	refresh(w)
}

func refresh(w http.ResponseWriter) {

	assigneValeurRetour()
	indexVars := valeurRetour

	t, err := template.ParseFiles("deux.html") //parse the html file index.html
	if err != nil {                                 // if there is an error
		log.Print("template parsing error: ", err) // log it
	}
	err = t.Execute(w, indexVars) //execute the template and pass it the indexVars struct to fill in the gaps
	if err != nil {               // if there is an error
		log.Print("template executing error: ", err) //log it
	}

}

func HomePage(w http.ResponseWriter, r *http.Request) {
	//	fmt.Println(w, "serving: %s\n", r.URL.Path)

	assigneValeurRetour()
	HomePageVars := valeurRetour

	t, err := template.ParseFiles("deux.html") //parse the html file homepage.html
	if err != nil {                                 // if there is an error
		log.Print("template parsing error: ", err) // log it
	}

	err = t.Execute(w, HomePageVars) //execute the template and pass it the HomePageVars struct to fill in the gaps
	if err != nil {                  // if there is an error
		log.Print("template executing error: ", err) //log it
	}
}

func assigneValeurRetour() {
	//fmt.Println("la valeur de la porte entree :   %t    %t    %d   \n", detecteur.PorteEntree.Statut, detecteur.PorteEntree.Etat, detecteur.PorteEntree.Valeur)

	if detecteur.PorteEntree.Statut == true {
		if detecteur.PorteEntree.Etat == true {
			valeurRetour.Pentree = "/images/red.png"
		} else {
			valeurRetour.Pentree = "/images/green.png"
		}
	} else {
		valeurRetour.Pentree = "/images/orange.png"
	}

	if detecteur.PorteArriere.Statut == true {
		if detecteur.PorteArriere.Etat == true {
			valeurRetour.Parriere = "/images/red.png"
		} else {
			valeurRetour.Parriere = "/images/green.png"
		}
	} else {
		valeurRetour.Parriere = "/images/orange.png"
	}

	if detecteur.PorteSousSol.Statut == true {
		if detecteur.PorteSousSol.Etat == true {
			valeurRetour.PsousSol = "/images/red.png"
		} else {
			valeurRetour.PsousSol = "/images/green.png"
		}
	} else {
		valeurRetour.PsousSol = "/images/orange.png"
	}

	if detecteur.ChambrePrincipale.Statut == true {
		if detecteur.ChambrePrincipale.Etat == true {
			valeurRetour.Cprincipale = "/images/red.png"
		} else {
			valeurRetour.Cprincipale = "/images/green.png"
		}
	} else {
		valeurRetour.Cprincipale = "/images/orange.png"
	}

	if detecteur.ChambreSecondaire.Statut == true {
		if detecteur.ChambreSecondaire.Etat == true {
			valeurRetour.Csecondaire = "/images/red.png"
		} else {
			valeurRetour.Csecondaire = "/images/green.png"
		}
	} else {
		valeurRetour.Csecondaire = "/images/orange.png"
	}

	if detecteur.SousSol.Statut == true {
		if detecteur.SousSol.Etat == true {
			valeurRetour.DSousSol = "/images/red.png"
		} else {
			valeurRetour.DSousSol = "/images/green.png"
		}
	} else {
		valeurRetour.DSousSol = "/images/orange.png"
	}

	if detecteur.ChambreSousSol.Statut == true {
		if detecteur.ChambreSousSol.Etat == true {
			valeurRetour.CsousSol = "/images/red.png"
		} else {
			valeurRetour.CsousSol = "/images/green.png"
		}
	} else {
		valeurRetour.CsousSol = "/images/orange.png"
	}

	if detecteur.Salon.Statut == true {
		if detecteur.Salon.Etat == true {
			valeurRetour.Dsalon = "/images/red.png"
		} else {
			valeurRetour.Dsalon = "/images/green.png"
		}
	} else {
		valeurRetour.Dsalon = "/images/orange.png"
	}

	if detecteur.Bureau.Statut == true {
		if detecteur.Bureau.Etat == true {
			valeurRetour.Dbureau = "/images/red.png"
		} else {
			valeurRetour.Dbureau = "/images/green.png"
		}
	} else {
		valeurRetour.Dbureau = "/images/orange.png"
	}

	if detecteur.ChauffeEau.Statut == true {
		if detecteur.ChauffeEau.Etat == true {
			valeurRetour.DchauffeEau = "/images/red.png"
		} else {
			valeurRetour.DchauffeEau = "/images/green.png"
		}
	} else {
		valeurRetour.DchauffeEau = "/images/orange.png"
	}

	if detecteur.AtelierEau.Statut == true {
		if detecteur.AtelierEau.Etat == true {
			valeurRetour.DatelierEau = "/images/red.png"
		} else {
			valeurRetour.DatelierEau = "/images/green.png"
		}
	} else {
		valeurRetour.DatelierEau = "/images/orange.png"
	}

	if detecteur.FumeeBas.Statut == true {
		if detecteur.FumeeBas.Etat == true {
			valeurRetour.DfumeeBas = "/images/red.png"
		} else {
			valeurRetour.DfumeeBas = "/images/green.png"
		}
	} else {
		valeurRetour.DfumeeBas = "/images/orange.png"
	}

	if detecteur.FumeeAtelier.Statut == true {
		if detecteur.FumeeAtelier.Etat == true {
			valeurRetour.DfumeeAtelier = "/images/red.png"
		} else {
			valeurRetour.DfumeeAtelier = "/images/green.png"
		}
	} else {
		valeurRetour.DfumeeAtelier = "/images/orange.png"
	}

	//HomePageVars := valeurRetour //store the date and time in a struct

}

func threadSysteme() {
	tcpAddr, err := net.ResolveTCPAddr("tcp", serviceSystemeTextIn)
	checkError(err)

	listener, err := net.ListenTCP("tcp", tcpAddr)

	checkError(err)
	var buf [2048]byte

	for {
		conn, err := listener.Accept()
		if err != nil {
			continue
		}

		n, err := conn.Read(buf[0:])

		var p structure.Equipements
		err = json.Unmarshal(buf[0:n], &p)
		if err != nil {
			panic(err)
		}

		detecteur = p
		DateHeureThreadConnexion = time.Now()
	}
}

func SendToSysteme(valeur string) {

	tcpAddr, err := net.ResolveTCPAddr("tcp", serviceSystemDataOut)
	if err != nil {
		//fmt.Println("Can't serislize %s \n", err)
	}

	conn, err := net.DialTCP("tcp", nil, tcpAddr)

	bytes, err := json.Marshal(valeur)
	if err != nil {
		//fmt.Println("Can't serislize")
	}

	x, err2 := conn.Write(bytes)
	//fmt.Println("hhhhhhhhhhhhhhhhhhhhhhhhhhhhhhhhhh %s  %s  \n", valeur, x)
	if err2 != nil {
		fmt.Printf("%s \n", x)
		return
	}
}

func checkError(err error) {
	if err != nil {
		//fmt.Fprintf(os.Stderr, "Fatal error: %s", err.Error())
		os.Exit(1)
	}
}
