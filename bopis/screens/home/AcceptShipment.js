import React, { useEffect, useState, useCallback } from 'react';
import { useDispatch, useSelector } from 'react-redux';
import {acceptShipment, fetchOrders, reset, registerPush} from "../../features/orders";
import * as Font from 'expo-font';
import {
  Container,
  Content,
  Card,
  CardItem, 
  Right, 
  Icon, 
  Left, 
  Body
} from 'native-base';
import {
  StyleSheet,
  View,
  Text,
  Pressable,
  ScrollView,
  RefreshControl
} from 'react-native';

const wait = (timeout) => {
  return new Promise(resolve => setTimeout(resolve, timeout));
}

const AcceptShipment = ({ navigation }) =>{
  const { orders} = useSelector((state) => state.orders)
  const dispatch = useDispatch()
  const [refreshing, setRefreshing] = useState(false);

  useEffect(() => {
    dispatch(fetchOrders())
  }, []);

  useEffect(() => {
    (async () => await Font.loadAsync({
      Roboto: require('native-base/Fonts/Roboto.ttf'),
      Roboto_medium: require('native-base/Fonts/Roboto_medium.ttf'),
    }))();
     }, [])

    const onRefresh = useCallback(() => {
    setRefreshing(true);
    dispatch(fetchOrders());
    wait(2000).then(() => setRefreshing(false));
  }, []);

  const handleAccept = (id, order) => {
      dispatch(acceptShipment(id));
      dispatch(reset());
      dispatch(fetchOrders())
      switch(order.status){
        case 'Open':
          {
            order.orderType === 'Bopis' ? (
              navigation.navigate(
                'Pick List', {
                    orderId: order.id,
                    orderNumber:order.orderID,
                    items: order.items
                })
            ) : (
              navigation.navigate(
                'Validate Stock', {
                    orderId: order.id,
                    orderNumber:order.orderID,
                    orderType: order.orderType,
                    items: order.items,
                    customerEmail: order.customerEmail,
                    parkingSpot: order.parkingSpot,
                    deliveryMethod: order.deliveryMethod,
                    vehicleDetails: order.vehicleDetails,
                    licensePlate: order.licensePlate,
                    orderStatus: order.status
                })
            )}
          break;
        case 'Shipment Accepted':
          {
            order.orderType === 'Bopis' ? (
              navigation.navigate(
                'Pick List', {
                    orderId: order.id,
                    orderNumber:order.orderID,
                    items: order.items
                }
            )
            ) :(
              navigation.navigate(
                'Validate Stock', {
                    orderId: order.id,
                    orderNumber:order.orderID,
                    orderType: order.orderType,
                    items: order.items,
                    customerEmail: order.customerEmail,
                    parkingSpot: order.parkingSpot,
                    deliveryMethod: order.deliveryMethod,
                    vehicleDetails: order.vehicleDetails,
                    licensePlate: order.licensePlate,
                    orderStatus: order.status
                })
            )
          }
          break;
        case 'Pick List Printed':
          navigation.navigate(
              'Validate Stock', {
                  orderId: order.id,
                  orderNumber:order.orderID,
                  items: order.items
              }
          )
          break;
        case 'Stock Validated':
          navigation.navigate(
              'Confirm Delivery', {
                orderId: order.id,
                orderNumber:order.orderID,
                orderType: order.orderType,
                items: order.items,
                customerEmail: order.customerEmail,
                parkingSpot: order.parkingSpot,
                deliveryMethod: order.deliveryMethod,
                vehicleDetails: order.vehicleDetails,
                licensePlate: order.licensePlate,
                orderStatus: order.status
              }
          )
          break;
      }
    }

  const reload = () => {
    dispatch(reset());
    dispatch(fetchOrders())
   }

  const renderItems = (items) => {
    return (
      <View>
      {
        items.map((e, idx) => <Text key={idx}>{e.quantity} - {e.name}</Text>)
      }
      </View>
    )
  }
   
    const renderCards = (orders) => {
      return (
      <View>
        {
          orders.map((order, idx) =>
          <Card style={order.status === 'Complete' ? styles.hide : null} key={idx}>
            <CardItem>
                <Icon name="receipt-outline" />
                <Body>
                  <Text>Order Number: </Text>
                  <Text note>{order.orderID}</Text>
                </Body>
            </CardItem>
            <CardItem>
                <Left>
                    { renderItems(order.items) }
                </Left>
                <Right>
                <Pressable onPress={() => handleAccept(order.id, order)} style={styles.acceptBtn}>
                    <Text style={styles.text}>{order.status === 'Open' ? 'Fulfill': 'Resume'}</Text>
                </Pressable>
                </Right>
              
            </CardItem>
            <CardItem>
              <Left>
                  <Icon name="reader-outline" />
                  <Text>Order Status</Text>
              </Left>
              <Right>
                <Text style={styles.open}>{order.status}</Text>
              </Right>
            </CardItem>
            <CardItem>
              <Left>
                  <Icon name="book-outline" />
                  <Text>Order Type</Text>
              </Left>
              <Right>
                <Text style={styles.open}>{order.orderType}</Text>
              </Right>
            </CardItem>
          </Card>
          )}
        </View>
      )
    }

    return (
     
        <Container>
        <ScrollView
          refreshControl={
            <RefreshControl
              refreshing={refreshing}
              onRefresh={onRefresh}
            />
          }>
          <Content>
              { renderCards(orders)}
          </Content>
          </ScrollView>
        </Container>
    );
    }

    const styles = StyleSheet.create({
      container: {
        flex: 1,
        alignItems: 'center',
        justifyContent: 'center'
      },
      myBtn: {
        height: 50,
        width: 400,
        backgroundColor:'#000',
        borderRadius:75,
        borderWidth: 1,
        margin:10,
        flex: 1,
        alignItems: 'center',
        justifyContent: 'center',
      },
      acceptBtn: {
        height: 40,
        padding: 0,
        width: 100,
        backgroundColor:'#000',
        borderRadius:80,
        borderWidth: 1,
        alignItems: 'center',
        justifyContent: 'center',
      },
      text: {
          color: 'white'
      },
      completed: {
          color: '#5cb85c'
      },
      open: {
          color: 'red'
      },
      hide: {
        display:'none'
      }
});

export default AcceptShipment;