import React, { useState, useEffect } from 'react';
import * as Font from 'expo-font';
import {
  StyleSheet,
  View,
  Text,
  Pressable,
  Image
} from 'react-native';
import { customerAccepted, reset, fetchOrders } from "../../features/orders";
import {
    Container,
    Content,
    Body
  } from 'native-base';
  import { useDispatch } from 'react-redux';




export default function ConfirmDelivery({ navigation, route }){
    const dispatch = useDispatch()
    const handleDelivery = (id) => {
        dispatch(customerAccepted(id));
        dispatch(reset());
        dispatch(fetchOrders())
        navigation.navigate(
            'Accept Shipment'
        )
      }

      useEffect(() => {
        (async () => await Font.loadAsync({
          Roboto: require('native-base/Fonts/Roboto.ttf'),
          Roboto_medium: require('native-base/Fonts/Roboto_medium.ttf'),
        }))();
         }, [])
    const 
    { 
      orderId, 
      orderNumber,
      orderType,
      customerEmail,
      parkingSpot,
      deliveryMethod,
      vehicleDetails,
      licensePlate,
      orderStatus 
    } = route.params;
    return (
        <Container>
            <Content>
                <Image
                    style={styles.storefront}
                    source={require('../../assets/rue21.jpg')} />
                  { orderType === 'Bopis' ?
                     (
                      <View>
                        <Body>
                          <View>
                            <Text style={styles.myTitle}>Order Number: </Text>
                            <Text style={styles.note}>{orderNumber}</Text>
                          </View>
                        </Body>
                        <Pressable 
                            title="Confirm Delivery" 
                            style={orderStatus === 'Stock Validated' ? styles.validateBtn : styles.disabledBtn} 
                            onPress={() => handleDelivery(orderId)}>
                            <Text style={styles.text}>Confirm Delivery</Text>
                        </Pressable>
                      </View>
                     )
                     :
                    ( 
                      <View>
                        <Body>
                          <View>
                            <Text style={styles.myTitle}>Order Number: </Text>
                            <Text style={styles.note}>{orderNumber}</Text>
                            <Text style={styles.myTitle}>Customer Email: </Text>
                            <Text style={styles.note}>{customerEmail}</Text>
                            <Text style={styles.myTitle}>Parking Spot: </Text>
                            <Text style={styles.note}>{parkingSpot}</Text>
                            <Text style={styles.myTitle}>Delivery Method: </Text>
                            <Text style={styles.note}>{deliveryMethod}</Text>
                            <Text style={styles.myTitle}>Vehicle Details: </Text>
                            <Text style={styles.note}>{vehicleDetails}</Text>
                            <Text style={styles.myTitle}>License Plate: </Text>
                            <Text style={styles.note}>{licensePlate}</Text>
                          </View>
                        </Body>
                        <Pressable 
                            disabled={orderStatus === 'Customer Curbside' ?  false : true}
                            title="Confirm Delivery" 
                            style={orderStatus === 'Customer Curbside' ? styles.validateBtn : styles.disabledBtn} 
                            onPress={() => handleDelivery(orderId)}>
                            <Text style={styles.text}>Confirm Delivery</Text>
                        </Pressable>
                      </View>
                    )
                   }
            </Content>
    </Container>
    );
  

    }
    const styles = StyleSheet.create({
      container: {
        flex: 1,
        alignItems: 'center',
        justifyContent: 'center'
      },
      validateBtn: {
        height: 50,
        width: 300,
        backgroundColor:'#000',
        borderRadius:75,
        margin:10,
        flex: 1,
        alignItems: 'center',
        justifyContent: 'center',
        alignSelf: 'center'
      },
      disabledBtn: {
        height: 50,
        width: 300,
        backgroundColor:'#808080',
        borderRadius:75,
        margin:10,
        flex: 1,
        alignItems: 'center',
        justifyContent: 'center',
        alignSelf: 'center'
      },
      text: {
        color: 'white'
    },
    myCheck:{
        marginRight: '10%'
    },
    myTitle:{
        fontSize:24,
        alignSelf: 'center',
        marginTop: '10%'
    },
    note:{
        fontSize:16,
        alignSelf: 'center',
        marginTop: 10,
        marginBottom: '10%'
    },
    myList:{
        fontSize:16,
        marginBottom: '15%'
    },
    storefront: {
        height: 250,
        width: 300,
        alignSelf: 'center',
        marginVertical: '10%',
        borderRadius:10
    }
}); 