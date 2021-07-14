import { GET_ORDER, GET_ORDER_FAIL, GET_ORDERS, GET_ORDERS_FAIL} from '../actions/types';

const initialState = {
    orders: [],
    order : {},
    error : 'Oops'
}

 export default function(state = initialState, action){
     const {type, payload } = action;

     switch(type){
         case GET_ORDER:
             return{
                 ...state,
                 order : payload,
                 error: ''
             }
        case GET_ORDER_FAIL:
            return{
                ...state,
                order : payload,
                error: 'Error getting an order'
            }
        case GET_ORDERS:
            return{
                ...state,
                order : payload,
                error: ''
            }
        case GET_ORDERS_FAIL:
            return{
                ...state,
                order : payload,
                error: 'Error getting all orders'
            }
        default:
            return state
     }
 }