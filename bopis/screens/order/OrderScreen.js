import React, { useState, useEffect, useCallback } from 'react';
import { useDispatch, useSelector } from 'react-redux';
import { fetchOrders, reset} from "../../features/orders";
import * as Font from 'expo-font';
import {
  Container,
  Content,
  Card,
  CardItem, 
  Right, 
  Icon, 
  Left, 
  Body,
  Header,
  Title
} from 'native-base';
import {
  StyleSheet,
  View,
  Text,
  Pressable,
  RefreshControl,
  ScrollView
} from 'react-native';


const wait = (timeout) => {
  return new Promise(resolve => setTimeout(resolve, timeout));
}

const OrderScreen = () =>{
  const { orders} = useSelector((state) => state.orders)
  const dispatch = useDispatch()
  const [refreshing, setRefreshing] = useState(false);

  useEffect(() => {
    dispatch(fetchOrders()) 
  }, [])

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

  const renderItems = (items) => {
    return (
      <View>
      {
        items.map((e, idx) => <Text key={idx} style={styles.darkText}>{e.quantity}  -  {e.name}</Text>)
      }
      </View>
    )
  }

  const reload = () => {
   dispatch(reset());
   dispatch(fetchOrders())
  }
   
    const renderCards = (orders) => {
      return (
      <View>
        {
          orders.map((order, idx) =>
          <Card key={idx}>
            <CardItem style={styles.cardItem}>
                <Icon name="receipt-outline" />
                <Body>
                  <Text style={styles.darkText}>Order Number: </Text>
                  <Text style={styles.darkText} note>{order.orderID}</Text>
                </Body>
              
            </CardItem>
            <CardItem style={styles.cardItem}>
              <Body>
                { renderItems(order.items) }
              </Body>
            </CardItem>
            <CardItem style={styles.cardItem}>
              <Left>
                  <Icon name="reader-outline" />
                  <Text style={styles.darkText}>Order Status</Text>
              </Left>
              <Right>
                <Text style={order.status === 'Complete' ? styles.completed : styles.open}>{order.status}</Text>
              </Right>
            </CardItem>
            <CardItem style={styles.cardItem}>
              <Left>
                  <Icon name="folder-outline" />
                  <Text style={styles.darkText}>Order Type</Text>
              </Left>
              <Right>
                <Text style={styles.darkText}>{order.orderType}</Text>
              </Right>
            </CardItem>
          </Card>
          )}
        </View>
      )
    }

    return (
      <>
      <Header style={styles.myBackground}>
        <Title style={styles.titleText}>Orders</Title>
      </Header>
      <Container>
        <ScrollView
          refreshControl={
            <RefreshControl
              refreshing={refreshing}
              onRefresh={onRefresh}
            />
          }>
        <Content>
          { renderCards(orders) } 
        </Content>
        </ScrollView>
      </Container>
      </>
    );
  

    }
    const styles = StyleSheet.create({
      container: {
        flex: 1,
        alignItems: 'center',
        justifyContent: 'center'
      },
      card: {
        marginTop:'10%'
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
      lightText: {
        color: 'white'
      },
      completed: {
        color: '#5cb85c'
      },
      open: {
          color: 'red'
      } ,
      cardItem: {
        borderBottomColor: '#d3d3d3',
        borderBottomWidth : 1,
      },
      darkText: {
        color: 'black'
      },
      titleText: {
        color: 'black',
        fontSize: 24,
        fontWeight: '600',
      },
      myBackground: {
        backgroundColor: 'white'
      }
});

export default OrderScreen;