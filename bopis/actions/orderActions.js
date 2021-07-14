import client from '../utils/client';
import {
    GET_ORDER,
    GET_ORDER_FAIL,
    GET_ORDERS,
    GET_ORDERS_FAIL
} from './types';

const url =  '/orders';

export const getOrder = (id) => {
    return dispatch => {
        dispatch({
            type: GET_ORDER,
            payload: client.get(`${url}/${id}`)
        })
    }
}
export const fetchOrders = () => dispatch =>{
    try {
        const res = await axios.get(`http://192.168.1.68:8000/orders`, config);
        dispatch({
            type: GET_ORDERS,
            payload: res.data
        });
    } catch (error) {
        console.log(`error: ${error}`)
        dispatch({
            type: GET_ORDERS_FAIL
        });
        
    }
}

export const getOrders = () =>{
    return dispatch => {
        dispatch({
            type: GET_ORDERS,
            payload: client.get(url)
        })
    }
}
