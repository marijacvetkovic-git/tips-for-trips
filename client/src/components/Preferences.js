import { useEffect,useState } from "react";
import axios from "axios";
import React from 'react';
import { Button, Checkbox, Col, Row,message } from 'antd';
// import { getUsername,getUserId } from "./utils";
import { useLocation } from 'react-router-dom';



const Preferences=()=>{
const [messageApi, contextHolder] = message.useMessage();
const loggedIn = () => {
    messageApi.open({
      type: 'success',
      content: 'You are registered!',
      duration: 3,
    });
    setTimeout(() => {
    window.location = "/home";
  }, 3000);

  };

const location = useLocation();

const [listOfHashtags,setListOfHashtags]=useState([])
const [checkedValues, setCheckedValues] = useState([]);
const [isButtonDisabled, setButtonDisabled] = useState(true);
const [idOfUser,setIdOfUser]=useState("")
const responseData = location.state;

useEffect(()=>{setIdOfUser(responseData["id"])},[])


const handleClick=()=>{
console.log(checkedValues)
console.log(idOfUser)
const idsOfHashtags=checkedValues.join(',');

const realtionshipWantsToSeeBody = {idOfUser,idsOfHashtags}
console.log(realtionshipWantsToSeeBody)
axios.post("http://127.0.0.1:5000/auth/createRelationship_WANTS_TO_SEE",realtionshipWantsToSeeBody)
.then(responce=>{
  if(responce.status===200)
  {
    loggedIn()
  }
})
 .catch(error=>{console.error('Error:', error);
     });


}
const onChange = (checkedValues) => {
  console.log('checked = ', checkedValues);
  setCheckedValues(checkedValues);
  setButtonDisabled(checkedValues.length < 3);


};

  useState(()=>{
    axios.get("http://127.0.0.1:5000/helpers/getHashtags")
    .then(responce=>{
      if(responce.status===200)
      {
        console.log(responce.data)
        setListOfHashtags(responce.data)
      }

    })
    .catch(error=>{console.error('Error:', error);
     });

  },[])
  return(
    <>
    <h1>What do you want to see?</h1>
    <section>
     <Checkbox.Group
    style={{
      width: '100%',
    }}
    onChange={onChange}
    value={checkedValues}
  >
    <Row>
      {listOfHashtags.map((item)=>(
        <Col span={8} key={item["id"]} >
        <Checkbox value={item["id"]}>
          {item["name"]} </Checkbox>
        </Col>
      ))}
    </Row>
  </Checkbox.Group>
  <Button onClick={handleClick} disabled={isButtonDisabled}>Finish</Button>
  </section>


    </>
  );

}
export default Preferences