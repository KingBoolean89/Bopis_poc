import React, { useState, useEffect } from "react";
import { useDispatch, useSelector } from 'react-redux';
import { login } from "../../features/user";
import { StatusBar } from "expo-status-bar";
import {
  StyleSheet,
  Text,
  View,
  Image,
  TextInput,
  TouchableOpacity,
} from "react-native";
 
const LoginScreen = () => {
    const [username, setUsername] = useState('');
    const [password, setPassword] = useState('');
    const dispatch = useDispatch()

    const onSubmit = e =>{
        e.preventDefault();
        const data = {"username": username, "password": password}
         dispatch(login(data))
    }
 
  return (
    <View style={styles.container}>
        <View style={styles.form}>
            <Image
            source={require('../../assets/favicon.png')}
            fadeDuration={0}
            style={styles.logo}
            />
            <StatusBar style="auto" />
            <View style={styles.inputView}>
                <TextInput
                style={styles.TextInput}
                placeholder="Username."
                placeholderTextColor="#000000"
                onChangeText={(username) => setUsername(username)}
                />
            </View>
        
            <View style={styles.inputView}>
                <TextInput
                style={styles.TextInput}
                placeholder="Password."
                placeholderTextColor="#000000"
                secureTextEntry={true}
                onChangeText={(password) => setPassword(password)}
                />
            </View>
            <TouchableOpacity onPress={(e) => onSubmit(e)} style={styles.loginBtn}>
                <Text style={styles.loginText}>LOGIN</Text>
            </TouchableOpacity>
        </View>
    </View>
  );
}
 
const styles = StyleSheet.create({
  container: {
    flex: 1,
    backgroundColor: "#fff",
    alignItems: "center",
    justifyContent: "center",
  },
  logo:{
    width: 70,
    height: 70,
    marginBottom:"40%",
    marginVertical:"30%",
    alignSelf:"center" 
  },
  form: {
    padding: "5%",
    width:"90%",
    height:"90%",
  },
  loginText:{
      color:"#fff"
  },
 
  inputView: {
    borderBottomWidth:2,
    borderBottomColor: "black",
    width: "100%",
    height: 45,
    marginBottom: 10,
    marginTop: 10,
    alignItems: "flex-start",
  },
 
  TextInput: {
    height: 50,
    flex: 1,
    padding: 10,
    marginLeft: 10,
  },
 
  forgot_button: {
    height: 30,
    marginBottom: 30,
  },
 
  loginBtn: {
    width: "100%",
    borderRadius: 25,
    height: 50,
    color:"#fff",
    alignItems: "center",
    justifyContent: "center",
    marginTop: 30,
    backgroundColor: "#000",
  },
});

export default LoginScreen;