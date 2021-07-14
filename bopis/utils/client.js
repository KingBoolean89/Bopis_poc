import axios from "axios";

export const client = axios.create({
  baseURL: "http://192.168.1.68:3000",
  headers: {
    "Content-Type": "application/json"
  }
})