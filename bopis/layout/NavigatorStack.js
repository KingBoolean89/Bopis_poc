import React from 'react';
import { NavigationContainer } from '@react-navigation/native';
import { createBottomTabNavigator } from '@react-navigation/bottom-tabs';
import HomeScreen from '../screens/home/HomeScreen';
import OrderScreen from '../screens/order/OrderScreen';
import { Icon } from 'native-base';
import  {useSelector, useDispatch}  from 'react-redux';
import { StatusBar } from "expo-status-bar";
import LoginScreen from '../screens/login/LoginScreen';


const Tab = createBottomTabNavigator();


function NavigatorStack() {
    const { isAuthenticated} = useSelector((state) => state.users)
    return (
        
            <NavigationContainer >
                {/* {
                    isAuthenticated ?
                    <Tab.Navigator 
                        tabBarOptions={{
                            activeTintColor: 'black',
                            inactiveTintColor: 'gray',
                            labelStyle: {fontSize:12}
                        }}>  
                        <Tab.Screen
                            name="Home" 
                            component={HomeScreen}
                            options={{
                            tabBarLabel: 'Home',
                            title: 'My home' ,
                            tabBarIcon: (() => <Icon name='home-outline' />)
                            }} />
                        <Tab.Screen 
                            name="Orders" 
                            component={OrderScreen}
                            options={{
                            tabBarLabel: 'Orders',
                            title: 'Orders',
                            tabBarIcon: (() => <Icon name='book-outline' />) 
                            }} />     
                    </Tab.Navigator> :
                    <LoginScreen />
                } */}
                <Tab.Navigator 
                        tabBarOptions={{
                            activeTintColor: 'black',
                            inactiveTintColor: 'gray',
                            labelStyle: {fontSize:12}
                        }}>  
                        <Tab.Screen
                            name="Home" 
                            component={HomeScreen}
                            options={{
                            tabBarLabel: 'Home',
                            title: 'My home' ,
                            tabBarIcon: (() => <Icon name='home-outline' />)
                            }} />
                        <Tab.Screen 
                            name="Orders" 
                            component={OrderScreen}
                            options={{
                            tabBarLabel: 'Orders',
                            title: 'Orders',
                            tabBarIcon: (() => <Icon name='book-outline' />) 
                            }} />     
                    </Tab.Navigator>
                
             </NavigationContainer>
         
    )
}

export default NavigatorStack;