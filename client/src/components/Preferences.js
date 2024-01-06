import { useEffect,useState } from "react";
import axios from "axios";
import React from 'react';
import { Button, Checkbox, Col, Row,message,Modal } from 'antd';
// import { getUsername,getUserId } from "./utils";
import { useLocation } from 'react-router-dom';



const Preferences=()=>{
const [messageApi, contextHolder] = message.useMessage();
const finishedRegistration = () => {
    messageApi.open({
      type: 'success',
      content: 'You are registered!',
      duration: 3,
    });
    setTimeout(() => {
    window.location = "/home";
  }, 3000);

  };

  const notFinishedRegistration = () => {
    messageApi.open({
      type: 'error',
      content: 'Your registration failed!',
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
const [loading, setLoading] = useState(false);
const [open, setOpen] = useState(true);

useEffect(()=>{setIdOfUser(responseData["id"])},[])
const handleCancel = () => {
    notFinishedRegistration()
  };

const handleClick=()=>{
setLoading(true);

console.log(checkedValues)
console.log(idOfUser)
const idsOfHashtags=checkedValues.join(',');

const realtionshipWantsToSeeBody = {idOfUser,idsOfHashtags}
console.log(realtionshipWantsToSeeBody)
axios.post("http://127.0.0.1:5000/auth/createRelationship_WANTS_TO_SEE",realtionshipWantsToSeeBody)
.then(responce=>{
  if(responce.status===200)
  {
    axios.post(`http://127.0.0.1:5000/auth/newUsercoldStartRecommendation/${idOfUser}`)
    .then(resp=>{
      if(resp.status===200)
      {
        setLoading(false);
        finishedRegistration()
      }
    })
     .catch(error=>{console.error('Error:', error);
     });
  
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
      <Modal
        open={open}
        title="Preferences"
        onOk={handleClick}
        onCancel={handleCancel}
        footer={[
          <Button key="back" onClick={handleCancel}>
            Cancle
          </Button>,
          <Button key="submit" type="primary" loading={loading} onClick={handleClick}  disabled={isButtonDisabled}>
            Submit
          </Button>
        ]}
      >
        {contextHolder}
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
  </section>
  </Modal>
    </>
  );

}
export default Preferences