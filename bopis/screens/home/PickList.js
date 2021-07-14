import React, { useEffect } from 'react';
import * as Font from 'expo-font';
import {
  StyleSheet,
  View,
  Text,
  Pressable
} from 'react-native';
import {
    Container,
    Content,
    List,
    Right, 
    Icon, 
    Left, 
    ListItem,
    Body
  } from 'native-base';
  import { useDispatch } from 'react-redux';
import { printPickList, reset, fetchOrders } from "../../features/orders";
import { createAndSavePDF } from '../../utils/pdf';
import { htmlContent } from '../../utils/Content';



export default function PickList({ route, navigation }){
  const dispatch = useDispatch()
  const { orderId, items, orderNumber } = route.params;

  useEffect(() => {
    (async () => await Font.loadAsync({
      Roboto: require('native-base/Fonts/Roboto.ttf'),
      Roboto_medium: require('native-base/Fonts/Roboto_medium.ttf'),
    }))();
     }, [])

  const handlePicking = (id) => {
      dispatch(printPickList(id));
      dispatch(reset());
      dispatch(fetchOrders())
      createAndSavePDF(htmlContent, items)
    }

    const renderList = (items) => {
        return( 
        <List style={styles.myList} >
            {
                items.map((item, idx) => 
                <ListItem key={idx}>
                    <Left><Text style={styles.listItem}>{item.quantity}</Text></Left>
                    <Right><Text style={styles.listItem}>{item.name}</Text></Right>
                </ListItem> )
            }
        </List>
        )}
    return (
      <Container>
          <Content>
            {/* <Text style={styles.myTitle} >Print Pick List</Text> */}
            <Body>
                <Text style={styles.myTitle}>Order Number: </Text>
                <Text style={styles.note}>{orderNumber}</Text>
            </Body>
            { renderList(items) }
            <Pressable title="Print List" style={styles.printBtn} onPress={() => handlePicking(orderId)}><Text style={styles.text}>Print</Text></Pressable>
            <Pressable title="Validate Stock" style={styles.validateBtn} onPress={() => navigation.navigate(
                    'Validate Stock', {
                        orderId: orderId,
                        orderNumber:orderNumber,
                        items: items
            
                    })}><Text style={styles.text}>Validate Stock</Text></Pressable>
        </Content>
      </Container>
    );
  

    }
    const styles = StyleSheet.create({
      printBtn: {
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
    listItem: {
        alignSelf: 'center'
    }
  
}); 