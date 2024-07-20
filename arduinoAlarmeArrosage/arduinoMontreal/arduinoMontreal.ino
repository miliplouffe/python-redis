#include <ArduinoJson.h>
#include <ArduinoJson.hpp>
#include <MQ2.h>

#include <Adafruit_MCP23X17.h>
#include "Timer.h"
#include "Math.h"
#include <string>


#define RELAY_1  4  // the Arduino pin, which connects to the relay 1
#define RELAY_2  5  // the Arduino pin, which connects to the relay 2
#define RELAY_3  6  // the Arduino pin, which connects to the relay 3
#define RELAY_4  7 // the Arduino pin, which connects to the relay 4



#define TIME_MSG_LEN  11   // time sync to PC is HEADER followed by unix time_t as ten ascii digits
#define TIME_HEADER  255   // Header tag for serial time sync message
#define DELAYERREUR 25
#define FEED_PIN 15  // MCP23XXX pin button is attached to

int number = 0;
int systemeArrosagePin = 8;
bool systemeDetectionPosition=false;
bool activationSystemeArrosage=false;
int debug = 0;

int pinChambrePrincipale=0;
int pinChambreSecondaire=1;
int pinBureau=2;
int pinSalon=3;
int pinSousSol=4;
int pinSalleVernis=5;
int pinPorteAvant=6;
int pinPorteArriere=7;
int pinPorteSousSol=8;
int pinSensorFumeeSalleBillard = 12;
int pinAlarmeSonore=14;
float valeurMax = 10;


const int pinEauAtelier=0;
const int pinSensorFumeeAtelier=1;
const int pinEauSalleLavage=2;
const int pinSensorPluie = 3;


    
struct DETECTEUR {
  int MouvChambrePrincipale;
  int MouvChambreSecondaire;
  int MouvBureau;
  int MouvSalon;
  int MouvSalleBillard;
  int MouvSalleVernis;
  int InterPorteAvant;
  int InterPorteArriere;
  int InterPorteSousSol;
  int DectEauAtelier;
  int DectEauSalleLavage;
  int DectFumeeAtelier;
  int DectFumeeSalleBillard;
  int DectEauPluie;
  int DectArrosageZone1;
  int DectArrosageZone2;
  int DectArrosageZone3;
  int DectArrosageZone4;
  
} Detecteur;

int delaiLecture=0;
Adafruit_MCP23X17 mcp;
String requete="";
unsigned long previousMillis = 0;        // will store last time LED was updated
unsigned long interval = 5000;  

void setup() {
  Serial.begin(115200); 
  
   if (!mcp.begin_I2C()) {
    Serial.println("Error.");
    //while (1);
  }


  // initialize Arduino pins pour les relais
  pinMode(RELAY_1, OUTPUT);
  pinMode(RELAY_2, OUTPUT);
  pinMode(RELAY_3, OUTPUT);
  pinMode(RELAY_4, OUTPUT);

  // si le mode est INPUT_PULLUP le port (pin) devient valeur High (1) 
  // si le mode est INPUT  le port (pin) devient Low (0)
  
  mcp.pinMode(FEED_PIN, OUTPUT);
  mcp.digitalWrite(FEED_PIN, HIGH);
 
  mcp.pinMode(pinChambrePrincipale,INPUT_PULLUP);         
  mcp.pinMode(pinChambreSecondaire,INPUT_PULLUP);
  mcp.pinMode(pinBureau,INPUT_PULLUP);       
  mcp.pinMode(pinSalon,INPUT_PULLUP);       
  mcp.pinMode(pinSousSol,INPUT_PULLUP);       
  mcp.pinMode(pinSalleVernis,INPUT_PULLUP);            
  mcp.pinMode(pinPorteAvant,INPUT_PULLUP);       
  mcp.pinMode(pinPorteArriere,INPUT_PULLUP);        
  mcp.pinMode(pinPorteSousSol,INPUT_PULLUP);       
  //mcp.pinMode(pinEauAtelier,INPUT_PULLUP);          
  //mcp.pinMode(pinEauSalleLavage,INPUT_PULLUP);           
  //mcp.pinMode(pinSensorPluie,INPUT_PULLUP);       
  
  //mcp.pinMode(pinSensorFumeeSalleBillard,INPUT_PULLUP); // Doit être à high. le sensor quand il depasse la limite il devient un ground (0)
  //mcp.pinMode(pinSensorFumeeAtelier,INPUT_PULLUP);       // Doit être à high. le sensor quand il depasse la limite il devient un ground (0)

  mcp.pinMode(pinAlarmeSonore, OUTPUT);
  mcp.digitalWrite(pinAlarmeSonore, LOW); 

  //pinMode(systemeArrosagePin, OUTPUT); 
  // setPinArduino(systemeArrosagePin, HIGH);
  //debug=false;

   //positionneRelaiGicleur(RELAY_1,HIGH);
    // initialize i2c as slave
}


void loop() {
  

  requete=receivedFromRaspberry();

  if (requete=="AlarmeSonore_ON"){
    // mcp.digitalWrite(pinAlarmeSonore, HIGH);
    }
  if (requete=="AlarmeSonore_OFF"){
     // mcp.digitalWrite(pinAlarmeSonore, LOW);
    }

  if (requete=="Gicleur_1_ON"){
      positionneRelaiGicleur(RELAY_1,HIGH);
      Detecteur.DectArrosageZone1=HIGH;
      delay(250);
    }

  if (requete=="Gicleur_1_OFF"){
      positionneRelaiGicleur(RELAY_1,LOW);
      Detecteur.DectArrosageZone1=LOW;
      delay(250);
  }


  if (requete=="Gicleur_2_ON"){
      positionneRelaiGicleur(RELAY_2,HIGH);
      Detecteur.DectArrosageZone2=HIGH;
      delay(250);
  }

  if (requete=="Gicleur_2_OFF"){
      positionneRelaiGicleur(RELAY_2,LOW);
      Detecteur.DectArrosageZone2=LOW;
      delay(250);
  }

  if (requete=="Gicleur_3_ON"){
      positionneRelaiGicleur(RELAY_3,HIGH);
      Detecteur.DectArrosageZone3=HIGH;
      delay(250);
  }


  if (requete=="Gicleur_3_OFF"){
      positionneRelaiGicleur(RELAY_3,LOW);
      Detecteur.DectArrosageZone3=LOW;
      delay(250);
  }


  if (requete=="Gicleur_4_ON"){
      positionneRelaiGicleur(RELAY_4,HIGH);
      Detecteur.DectArrosageZone4=HIGH;
      delay(250);

  }

  if (requete=="Gicleur_4_OFF"){
      positionneRelaiGicleur(RELAY_4,LOW);
      Detecteur.DectArrosageZone4=LOW;
      delay(250);
  }


  Detecteur.MouvChambrePrincipale=getDetecteurStatut(pinChambrePrincipale);
  Detecteur.MouvChambreSecondaire=getDetecteurStatut(pinChambreSecondaire);
  Detecteur.MouvBureau=getDetecteurStatut(pinBureau);
  Detecteur.MouvSalon=getDetecteurStatut(pinSalon);
  Detecteur.MouvSalleBillard=getDetecteurStatut(pinSousSol);
  Detecteur.MouvSalleVernis=getDetecteurStatut(pinSalleVernis);
  Detecteur.InterPorteAvant=getDetecteurStatut(pinPorteAvant);
  Detecteur.InterPorteArriere=getDetecteurStatut(pinPorteArriere);
  Detecteur.InterPorteSousSol=getDetecteurStatut(pinPorteSousSol);
  Detecteur.DectEauAtelier=getPinStatut(pinEauAtelier);
  Detecteur.DectEauSalleLavage=getPinStatut(pinEauSalleLavage);
  // Detecteur.DectEauPluie=getPinStatut(pinSensorPluie);

  //Detecteur.DectFumeeSalleBillard=getDetecteurStatut(pinSensorFumeeSalleBillard);
  Detecteur.DectFumeeAtelier=getPinStatut(pinSensorFumeeAtelier);

  Detecteur.DectArrosageZone1=getStatutOutputPin(RELAY_1);
  Detecteur.DectArrosageZone2=getStatutOutputPin(RELAY_2);
  Detecteur.DectArrosageZone3=getStatutOutputPin(RELAY_3);
  Detecteur.DectArrosageZone4=getStatutOutputPin(RELAY_4);
  Detecteur.DectEauPluie=0.0;
 
  delay(250);
  assigneValeursAuxVariables();
 
  //Serial.println("passe 1");
   requete="";
}

String receivedFromRaspberry() {

    String line="";
    line = Serial.readStringUntil('\n');
    delay(50);
    return line;

}

int getDetecteurStatut(int pinNo){
 int resultat=0;

resultat=mcp.digitalRead(pinNo);

    
 delay(15);
 return resultat; 
}


int getPinStatut(int pinNo){
  float resultat;
  
    resultat = analogRead(pinNo);  
    if (resultat > 800){
      return 0;
      }
      else{
          return 1;
      }
}
   
  

// statut du gicleur d arrosage
float getStatutOutputPin(int pin){
  
  uint8_t bit = digitalPinToBitMask(pin);
  uint8_t port = digitalPinToPort(pin);
  if (port == NOT_A_PIN) 
    return LOW;

  return (*portOutputRegister(port) & bit) ? HIGH : LOW;
  
}

void setPinArduino(int pinNo, bool valeur){

  if (valeur==true){
    digitalWrite(pinNo, HIGH);
  }
  else{
    digitalWrite(pinNo, LOW);   
  }
}

void positionneRelaiGicleur(int relayGicleur, int valeur){
  digitalWrite(relayGicleur, valeur); 
  }

void assigneValeursAuxVariables(){
    DynamicJsonDocument doc(400);
    char output[400];

    doc["MouvChambrePrincipale"]=Detecteur.MouvChambrePrincipale;
    doc["MouvChambreSecondaire"]=Detecteur.MouvChambreSecondaire;
    doc["MouvBureau"]=Detecteur.MouvBureau;
    doc["MouvSalon"]=Detecteur.MouvSalon;
    doc["MouvSalleBillard"]=Detecteur.MouvSalleBillard;
    doc["MouvSalleVernis"]=Detecteur.MouvSalleVernis;
    doc["InterPorteAvant"]=Detecteur.InterPorteAvant;
    doc["InterPorteArriere"]=Detecteur.InterPorteArriere;
    doc["InterPorteSousSol"]=Detecteur.InterPorteSousSol;
    doc["DectEauAtelier"]=Detecteur.DectEauAtelier;
    doc["DectEauSalleLavage"]=Detecteur.DectEauSalleLavage;
    doc["DectFumeeAtelier"]=Detecteur.DectFumeeAtelier;
    doc["DectFumeeSalleBillard"]=Detecteur.DectFumeeSalleBillard;
    doc["DectEauPluie"]=Detecteur.DectEauPluie;
    doc["DectArrosageZone1"]=Detecteur.DectArrosageZone1;
    doc["DectArrosageZone2"]=Detecteur.DectArrosageZone2;
    doc["DectArrosageZone3"]=Detecteur.DectArrosageZone3;
    doc["DectArrosageZone4"]=Detecteur.DectArrosageZone4;



    serializeJson(doc, output);
    Serial.println(output);
 
}
