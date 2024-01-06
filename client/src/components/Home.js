import { useEffect, useState } from "react";
import { useNavigate } from 'react-router-dom';
import axios from "axios";
import {getUserId} from "../utils"
import { Card,Space } from 'antd';

const { Meta } = Card;
const cardStyle = {
  width: 620,
};
const imgStyle = {
  display: 'block',
  width: 273,
};

const Home=()=>{
    const navigate = useNavigate();

    const [listOfAttractions,setListOfAttractions]=useState([])
    useEffect(()=>{
        console.log(localStorage.getItem("token"))
        if(localStorage.getItem("token")===null)
        {
            axios.get('http://127.0.0.1:5000/helpers/returnMostRecommendedAttractions')
            .then(responce=>{
                if(responce.status===200)
                {
                console.log(responce.data["listOfAttractions"])
                setListOfAttractions(responce.data["listOfAttractions"])
               
                }})
            .catch(error=>{console.error('Error:', error);
     });
        }
        else
        {
            const userId=getUserId()
            console.log(userId)
            console.log(localStorage.getItem("token"))
            axios.get(`http://127.0.0.1:5000/user/recommend/${userId}`,{ headers: { Authorization: `Bearer ${localStorage.getItem("token")}` } })
            .then(responce=>{
                if(responce.status===200)
                {
                  console.log(responce.data)

               // console.log(responce.data["listOfAttractions"])
                setListOfAttractions(responce.data)
                }})
            .catch(error=>{console.error('Error:', error);
     });
              

        }
    },[])

    const handleOnClick=(id)=>{
        console.log(id)
        navigate('/attraction', { state: id });
    }
   
    return(
        <>
         <Space size={[8, 16]} wrap>
            {listOfAttractions && listOfAttractions.map((item) => (
                  <Card
                  hoverable
                  value={item["id"]}
                  id={item["id"]}
                  style={{
                    width: 240,
                  }}
                  onClick={()=>handleOnClick(item["id"])}

                  cover={<img alt="example" src="https://os.alipayobjects.com/rmsportal/QBnOOoLaAfKPirc.png" />}
                >
                  <Meta title={item["name"]} />
                </Card>
              ))}
          </Space>
        </>
    );
}
export default Home;