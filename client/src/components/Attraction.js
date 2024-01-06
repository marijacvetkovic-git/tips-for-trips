import { useState } from 'react';
import { useLocation } from 'react-router-dom';
import axios from "axios";

const Attraction=()=>{

const location = useLocation();
const attractionId = location.state;

useState(()=>{
    console.log(localStorage.getItem("token"))
    axios.get(`http://127.0.0.1:5000/helpers/returnAttraction/${attractionId}`)
    .then(responce=>{
        if(responce.status===200)
        {
            console.log(responce.data)
        }
    })

},[])
    return(
        <>cao
        </>
    );
}
export default Attraction