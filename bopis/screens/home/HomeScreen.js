import React, { useEffect } from 'react';
import { createStackNavigator } from '@react-navigation/stack';
import {
  StyleSheet,
  View,
  Text
} from 'react-native';
import * as Font from 'expo-font';
import PickList from "./PickList";
import AcceptShipment from "./AcceptShipment";
import ConfirmDelivery from "./ConfirmDelivery";
import ValidateStock from "./ValidateStock"



const Stack = createStackNavigator();

export default function HomeScreen(){

  useEffect(() => {
    (async () => await Font.loadAsync({
      Roboto: require('native-base/Fonts/Roboto.ttf'),
      Roboto_medium: require('native-base/Fonts/Roboto_medium.ttf'),
    }))();
     }, [])

    return (
      <Stack.Navigator>
        <Stack.Screen name="Accept Shipment" component={AcceptShipment} 
        options={{
          title: 'Home',
          headerTitleStyle: {
            fontSize: 24,
            alignSelf: 'center',
            marginBottom: '7%'

          }
        }} />
        <Stack.Screen name="Pick List" component={PickList}
        options={{
          title: 'Pick List',
          headerTitleStyle: {
            fontSize: 24,
            alignSelf: 'center'
          }
        }} />
        <Stack.Screen name="Validate Stock" component={ValidateStock}
        options={{
          title: 'Validate Stock',
          headerTitleStyle: {
            fontSize: 24,
            alignSelf: 'center'
          }
        }} />
        <Stack.Screen name="Confirm Delivery" component={ConfirmDelivery}
        options={{
          title: 'Delivery Confirmation',
          headerTitleStyle: {
            fontSize: 24,
            alignSelf: 'center'
          }
        }} />
    </Stack.Navigator>
    );
  

    }
    const styles = StyleSheet.create({
      container: {
        flex: 1,
        alignItems: 'center',
        justifyContent: 'center'
      },
  
}); 
