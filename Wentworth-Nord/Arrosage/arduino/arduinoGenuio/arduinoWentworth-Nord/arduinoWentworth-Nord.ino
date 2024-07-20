// nouveau arduino wentworth-nord

#include <ArduinoJson.h>
#include <ArduinoJson.hpp>
#include <MQ2.h>

#include "Timer.h"
#include "Math.h"
#include <string>


#define TIME_MSG_LEN  11   // time sync to PC is HEADER followed by unix time_t as ten ascii digits
#define TIME_HEADER  255   // Header tag for serial time sync message
#define DELAYERREUR 25

#define TIME_MSG_LEN  11   // time sync to PC is HEADER followed by unix time_t as ten ascii digits
#define TIME_HEADER  255   // Header tag for serial time sync message
#define DELAYERREUR 25
#define FEED_PIN 15  // MCP23XXX pin button is attached to

// Serial.println(bitRead(PORTD,3)); //Reads bit 3 of register PORTD which contains the current state (high/low) of pin 3.

int sensorAnalogPin = A1;
int sensorMqPin = A0;
int detecteurEauElectriquePin=A3;
int detecteurEauTraitementPin=A4;
int detecteurMouvementPin=A5;
int detecteurPanneElectriquePinOut=5;
int detecteurPanneElectriquePinIn=A2;
int arrosage_RELAY_1 = 7;
bool systemeDetectionPosition=false;
bool activationSystemeArrosage=false;
int debug = 0;


struct DETECTEUR {
  float Prop;
  float Co;
  float Fumee;
  float Mouvement;
  float EauElectrique;
  float EauTraitement;
  float PanneElectrique;
  int DectArrosageZone1;
  int DectArrosageZone2;
  int DectArrosageZone3;
  int DectArrosageZone4;
  float Temperature;

}  Detecteur;

MQ2 mq2(sensorMqPin);
String data="";

int delaiLecture=0;
String requete="";
unsigned long previousMillis = 0;        // will store last time LED was updated
unsigned long interval = 5000;  

//  ------------------------------------
void setup() {
  Serial.begin(115200); // start serial for output
  mq2.begin();

  pinMode(detecteurPanneElectriquePinOut, INPUT_PULLUP);
  //digitalWrite(detecteurPanneElectriquePinOut, HIGH);
  pinMode(detecteurPanneElectriquePinIn, INPUT);
  
  pinMode(detecteurEauElectriquePin, INPUT);
  pinMode(detecteurEauTraitementPin, INPUT);
  pinMode(detecteurMouvementPin, INPUT);
  
  pinMode(arrosage_RELAY_1, OUTPUT); 
  setPinArduino(arrosage_RELAY_1, LOW);
  debug=false;
}

//  ------------------------------------
void loop() {

  // si la requete =  53 arrete le gicleur avec la pin à high pour que le relai soit en position ouvert
 
  if (requete=="53"){
    setPinArduino(arrosage_RELAY_1, HIGH);
  }
  
  // si la requete =  54 demarre le gicleur avec la pin à low pour que le relai soit en position fermé
  if (requete=="52"){
    setPinArduino(arrosage_RELAY_1, LOW);
  }
  
  if (requete=="97"){
    debug=1;
  }
  if (requete=="98"){
    debug=0;
  }
   
 if (millis() - previousMillis > interval) {


    Serial.println();
  
    previousMillis += interval;  
    assigneValeursAuxVariables();
  }  
    
   previousMillis += interval;
    
   delay(500);

  Detecteur=getMq2Valeur(Detecteur);
  
  Detecteur.Mouvement=getDetecteurStatut(detecteurMouvementPin);
  Detecteur.EauTraitement=getDetecteurStatut(detecteurEauTraitementPin);
  Detecteur.EauElectrique=getDetecteurStatut(detecteurEauElectriquePin);
  Detecteur.PanneElectrique= getDetecteurStatut(detecteurPanneElectriquePinIn);
  Detecteur.Temperature=Temperature(sensorAnalogPin);
  Detecteur.DectArrosageZone1=getStatutOutputPin(arrosage_RELAY_1);
  
 
  delay(50);
  assigneValeursAuxVariables();
  //Serial.println("passe 1");

  requete=receivedFromRaspberry();
  positionneRelaiGicleur(arrosage_RELAY_1,LOW);
  if (requete=="Gicleur_1_ON"){
      positionneRelaiGicleur(arrosage_RELAY_1,HIGH);
      // Detecteur.DectArrosageZone1=HIGH;
      
    }

  if (requete=="Gicleur_1_OFF"){
      positionneRelaiGicleur(arrosage_RELAY_1,LOW);
      // Detecteur.DectArrosageZone1=LOW;
    }
    
   requete="";

}

String receivedFromRaspberry() {

    String line="";
    line = Serial.readStringUntil('\n');
    delay(50);
    return line;

}


//  ------------------------------------
int getDetecteurStatut(int pinNo){
  
  int value = digitalRead(pinNo);
  return value;
}

//  ------------------------------------
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
   
  
//  ------------------------------------
// statut du gicleur d arrosage
float getStatutOutputPin(int pin){
  
  uint8_t bit = digitalPinToBitMask(pin);
  uint8_t port = digitalPinToPort(pin);
  if (port == NOT_A_PIN) 
    return LOW;

  return (*portOutputRegister(port) & bit) ? HIGH : LOW;
  
}

//  ------------------------------------
void setPinArduino(int pinNo, bool valeur){

  if (valeur==true){
    digitalWrite(pinNo, HIGH);
  }
  else{
    digitalWrite(pinNo, LOW);   
  }
}

//  ------------------------------------
DETECTEUR getMq2Valeur(DETECTEUR Detecteur){

  float* values= mq2.read(false); //set it false if you don't want to print the values in the Serial
  //Propane = values[0];
  Detecteur.Prop = mq2.readLPG();
  //co = values[1];
  Detecteur.Co = mq2.readCO();
  //smoke = values[2];
  Detecteur.Fumee = mq2.readSmoke();
  
  return Detecteur;
 
}


//  ------------------------------------
float Temperature(int sensorAnalogPin){
  //getting the voltage reading from the temperature sensor
   int reading = analogRead(sensorAnalogPin);  
   
   //Serial.print(reading); Serial.println(" volts 1");
   // converting that reading to voltage, for 3.3v arduino use 3.3
   float voltage = reading  * 5.0;
   voltage /= 1024.0; 
   
   // print out the voltage
   //Serial.print(voltage); Serial.println(" volts 2");
   
   // now print out the temperature
   float temperatureC = (voltage - 0.5) * 100 ;  //converting from 10 mv per degree wit 500 mV offset
                                                 //to degrees ((voltage - 500mV) times 100)
  // Serial.print(temperatureC); Serial.println(" degrees C");
   
   // now convert to Fahrenheit
   float temperatureF = (temperatureC * 9.0 / 5.0) + 32.0;
   //Serial.print(temperatureF); Serial.println(" degrees F");
  
   if (debug==1){
    Serial.print("Detecteur de temperature reading : ");
    Serial.print(reading);
    Serial.print("   ");
    Serial.print("voltage : ");
    Serial.print(voltage);
    Serial.print("   ");
    Serial.print("temperature : ");
    Serial.print(temperatureC);
    Serial.println();   
   }
   
   return temperatureC;
}

//  ------------------------------------
void positionneRelaiGicleur(int relayGicleur, int valeur){
  digitalWrite(relayGicleur, valeur); 
  }

//  ------------------------------------
void assigneValeursAuxVariables(){
    DynamicJsonDocument doc(400);
    char output[400];

 
    doc["DateHeure"] = "2024-12-22 8:00:00";
    doc["Prop"]=Detecteur.Prop;
    doc["Co"]=Detecteur.Co;
    doc["Fumee"]=Detecteur.Fumee;
    doc["Temperature"]=Detecteur.Temperature;
    doc["Mouvement"]= Detecteur.Mouvement;
    doc["EauElectrique"] = Detecteur.EauElectrique;
    doc["EauTraitement"] = Detecteur.EauTraitement;
    doc["PanneElectrique"] = Detecteur.PanneElectrique;
    doc["DectArrosageZone1"]=Detecteur.DectArrosageZone1;
    doc["DectArrosageZone2"]=Detecteur.DectArrosageZone2;
    doc["DectArrosageZone3"]=Detecteur.DectArrosageZone3;
    doc["DectArrosageZone4"]=Detecteur.DectArrosageZone4;
  
    serializeJson(doc, output);
    Serial.println(output);

}
