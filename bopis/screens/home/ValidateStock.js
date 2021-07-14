import React, { useState, useEffect } from 'react';
import * as Font from 'expo-font';
import {
  StyleSheet,
  View,
  Text,
  Pressable
} from 'react-native';
import { validateStock, reset, fetchOrders } from "../../features/orders";
import {
    Container,
    Content,
    Right, 
    Left,
    Picker, 
    ListItem,
    Body
  } from 'native-base';
  import { useDispatch } from 'react-redux';


export default function ValidateStock({ navigation, route}){
    const { 
            orderId, 
            items, 
            orderNumber, 
            orderType, 
            customerEmail, 
            parkingSpot, 
            deliveryMethod,
            vehicleDetails,
            licensePlate,
            orderStatus
          } = route.params;
    const dispatch = useDispatch()
    const [selected, setSelected] = useState("key0")

    useEffect(() => {
      (async () => await Font.loadAsync({
        Roboto: require('native-base/Fonts/Roboto.ttf'),
        Roboto_medium: require('native-base/Fonts/Roboto_medium.ttf'),
      }))();
       }, [])

    const handleStock = (id) => {
        dispatch(validateStock(id));
        dispatch(reset());
        dispatch(fetchOrders())
          navigation.navigate(
            'Confirm Delivery', {
                orderId: orderId,
                orderNumber:orderNumber,
                orderType: orderType, 
                customerEmail: customerEmail, 
                parkingSpot: parkingSpot, 
                deliveryMethod: deliveryMethod,
                vehicleDetails: vehicleDetails,
                licensePlate: licensePlate,
                orderStatus: orderStatus
            }
        )
      }
     const onValueChange = (value) =>
      {
        setSelected({
          selected: value
        });
      }

    const renderBoxes = (items) => {
        return(
            <View style={styles.myList}>
            {
                items.map((item, idx) => 
                <ListItem key={idx}>
                    <Left><Text>{item.name}</Text></Left>
                    <Right>
                        <Picker
                            note
                            mode="dropdown"
                            style={{ width: 150, color: 'black' }}
                            selectedValue={selected}
                            onValueChange={() => onValueChange(selected)}
                            >
                            <Picker.Item label="In Stock" value="key0" />
                            <Picker.Item label="Partial Stock" value="key1" />
                        </Picker>
                    </Right>
                </ListItem>
                )}
            </View>
        )
    }

    return (
      <Container>
          <Content>
          <Body>
                <Text style={styles.myTitle}>Order Number: </Text>
                <Text style={styles.note}>{orderNumber}</Text>
            </Body>
            { renderBoxes(items) }
            <Pressable title="Validate Stock" style={styles.validateBtn} onPress={() => handleStock(orderId)}><Text style={styles.text}>Confirm</Text></Pressable>
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
      text: {
        color: 'white'
    },
    myCheck:{
        marginRight: '10%'
    },
    myTitle:{
        fontSize:24,
        alignSelf: 'center',
        marginTop: '15%'
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
}); 