# arduino ancien  Wenworth-nord


#include <MQ2.h>
#include "Timer.h"
#include "Math.h"
#include <ArduinoJson.h>
#include <ArduinoJson.hpp>


#define RELAY1 9

#define TIME_MSG_LEN  11   // time sync to PC is HEADER followed by unix time_t as ten ascii digits
#define TIME_HEADER  255   // Header tag for serial time sync message
#define DELAYERREUR 25

int number = 0;
int sensorAnalogPin = A1;
int sensorMqPin = A0;
int detecteurEauElectriquePin=A3;
int detecteurEauTraitementPin=A4;
int detecteurMouvementPin=A5;
int detecteurPanneElectriquePinOut=5;
int detecteurPanneElectriquePinIn=A2;
int systemeArrosagePin = 8;
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
  float Arrosage;
  float Temperature;

}  Temp;

MQ2 mq2(sensorMqPin);
String data="";
String requete="";
int delaiLecture=0;

unsigned long previousMillis = 0;        // will store last time LED was updated
unsigned long interval = 5000;  

 
void setup() {
  Serial.begin(9600); // start serial for output
  mq2.begin();

  pinMode(detecteurPanneElectriquePinOut, INPUT_PULLUP);
  //digitalWrite(detecteurPanneElectriquePinOut, HIGH);
  pinMode(detecteurPanneElectriquePinIn, INPUT);
  
  pinMode(detecteurEauElectriquePin, INPUT);
  pinMode(detecteurEauTraitementPin, INPUT);
  pinMode(detecteurMouvementPin, INPUT);
  
  pinMode(systemeArrosagePin, OUTPUT); 
  setPinArduino(systemeArrosagePin, HIGH);
  debug=false;

  
    // initialize i2c as slave
}

void loop() {


  // si la requete =  4 arrete le gicleur avec la pin à high pour que le relai soit en position ouvert
  if (requete=="53"){
    setPinArduino(systemeArrosagePin, HIGH);
  }
  
  // si la requete =  5 demarre le gicleur avec la pin à low pour que le relai soit en position fermé
  if (requete=="52"){
    setPinArduino(systemeArrosagePin, LOW);
  }
  
  if (requete=="97"){
    debug=1;
  }
  if (requete=="98"){
    debug=0;
  }
   
 if (millis() - previousMillis > interval) {
   Serial.print("dans assign ");

    Serial.println();

    previousMillis += interval;  
    assigneValeursAuxVariables();
  }  
    
   previousMillis += interval;
    
   delay(500);
   requete="";
}


float getPinStatut(int pinNo){
  float resultat;
  
    resultat = analogRead(pinNo);  
    return resultat;
  }

// statut du gicleur d arrosage
float getStatutOutputPin(int pin){
  int resultat=0;
  int resultatFloat=0.0;
  
  resultatFloat = digitalRead(pin);
  
  if (resultatFloat == 0){
    resultatFloat=1.0;
  }else {resultatFloat=0.0;}
  
  return resultatFloat;
  
}

void setPinArduino(int pinNo, bool valeur){

  if (valeur==true){
    digitalWrite(pinNo, HIGH);
  }
  else{
    digitalWrite(pinNo, LOW);   
  }
  
 
}

DETECTEUR getMq2Valeur(){
  DETECTEUR valeur;
  float* values= mq2.read(false); //set it false if you don't want to print the values in the Serial
  //Propane = values[0];
  valeur.Prop = mq2.readLPG();
  //co = values[1];
  valeur.Co = mq2.readCO();
  //smoke = values[2];
  valeur.Fumee = mq2.readSmoke();
 
  return valeur;
  
}

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

void assigneValeursAuxVariables(){
    DynamicJsonDocument doc(250);
    char output[250];
    
    Temp=getMq2Valeur();
    
    Temp.Mouvement=getPinStatut(detecteurMouvementPin);
    Temp.EauTraitement=getPinStatut(detecteurEauTraitementPin);
    Temp.EauElectrique=getPinStatut(detecteurEauElectriquePin);
    Temp.PanneElectrique= getPinStatut(detecteurPanneElectriquePinIn);
    Temp.Arrosage=getStatutOutputPin(systemeArrosagePin);
    Temp.Temperature=Temperature(sensorAnalogPin);

 
    doc["DateHeure"] = "2024-12-22 8:00:00";
    doc["Prop"]=Temp.Prop;
    doc["Co"]=Temp.Co;
    doc["Fumee"]=Temp.Fumee;
    doc["Temperature"]=Temp.Temperature;
    doc["Mouvement"]= Temp.Mouvement;
    doc["EauElectrique"] = Temp.EauElectrique;
    doc["EauTraitement"] = Temp.EauTraitement;
    doc["PanneElectrique"] = Temp.PanneElectrique;
    doc["Arrosage"] = Temp.Arrosage; 
  
      serializeJson(doc, output);
      Serial.println(output);

   
   
  if (debug==1){
    
    Serial.print(" PanneElectrique ");Serial.print(Temp.PanneElectrique);Serial.println();
    Serial.print(" Co ");Serial.print(Temp.Co);Serial.println();
    Serial.print(" Fumee ");Serial.print(Temp.Fumee);Serial.println();
    Serial.print(" Temperature ");Serial.print(Temp.Temperature);Serial.println();    
    Serial.print(" Mouvement ");Serial.print(Temp.Mouvement);Serial.println();
    Serial.print(" EauElectrique ");Serial.print(Temp.EauElectrique);Serial.println();
    Serial.print(" EauTraitement ");Serial.print(Temp.EauTraitement);Serial.println(); 
    Serial.print(" Arrosage ");Serial.print(Temp.Arrosage);Serial.println();
    Serial.print(" Code envoye page web ");Serial.print(requete);Serial.println(); 
  }
    
}

void serialEvent() {
  
   // Serial.println(" valeur de la requete 1" + requete);
    requete = (String)Serial.read();
    // add it to the inputString:
    
    delay(50);
   // serializeJson(doc, Serial);
    //Serial.println(" valeur de la requetec 2" + requete);
    
}
