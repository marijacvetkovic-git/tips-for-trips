import React,{ useState } from 'react';
import { Button, Checkbox, Form, Input,Modal,message } from 'antd';
import axios from "axios";


const LogIn = () => {

const [username,setUsername]=useState("")
const [password,setPassword]=useState("")
const [isError,setIsError]=useState("")
const [latitude,setLatitude]=useState(0)
const [longitude,setLongitude]=useState(0)


const [isModalOpen, setIsModalOpen] = useState(true);

const [messageApi, contextHolder] = message.useMessage();
const loggedIn = () => {
    messageApi.open({
      type: 'success',
      content: 'You are logged in!',
      duration: 3,
    });
    setTimeout(() => {
    window.location = "/home";
  }, 3000);

  };
// const onFinish = (values) => {
//   console.log('Success:', values);
// };

const handleOk = () => {
  axios.get(`http://127.0.0.1:5000/auth/login/${username}/${password}/${latitude}/${longitude}`)
  .then(responce=>{
    if(responce.status===200)
    {
      console.log(responce.data["token"])
      localStorage.setItem("token", responce.data["token"]);

      loggedIn()
      //setIsModalOpen(false);
      // kada dodam windows.locatioon nece da mi se vidi ova poruka za login
    }
    else if (responce.status===206)
    {
      setIsError(responce.data["message"])
    }
  })
  };
  const handleCancel = () => {
    setIsModalOpen(false);
    window.location="/home"
  };

   useState(() => {
     if ("geolocation" in navigator) {
       // Get the user's current location
       navigator.geolocation.getCurrentPosition(
         function (position) {
           // The user's latitude and longitude are in position.coords.latitude and position.coords.longitude
           const Clatitude = position.coords.latitude;
           const Clongitude = position.coords.longitude;
           setLatitude(Clatitude);
           setLongitude(Clongitude);

           console.log(`Latitude: ${Clatitude}, Longitude: ${Clongitude}`);
         },
         function (error) {
           // Handle errors, if any
           switch (error.code) {
             case error.PERMISSION_DENIED:
               console.error("User denied the request for geolocation.");
               break;
             case error.POSITION_UNAVAILABLE:
               console.error("Location information is unavailable.");
               break;
             case error.TIMEOUT:
               console.error("The request to get user location timed out.");
               break;
             case error.UNKNOWN_ERROR:
               console.error("An unknown error occurred.");
               break;
           }
         }
       );
     } else {
       console.error("Geolocation is not available in this browser.");
     }
   }, []);
  return (
    <Modal
      title="Log In now!"
      open={isModalOpen}
      onOk={handleOk}
      onCancel={handleCancel}
    >
      {contextHolder}
      {/* <section className='wrapper'> */}
      <Form
        name="basic"
        className="wrapper"
        labelCol={{
          span: 8,
        }}
        wrapperCol={{
          span: 16,
        }}
        style={{
          maxWidth: 600,
          justifyContent: "center",
          alignItems: "center",
        }}
        initialValues={{
          remember: true,
        }}
        // onFinish={handleOk}
        // onFinishFailed={onFinishFailed}
        autoComplete="off"
      >
        <div style={{marginLeft:"100px"}}>
          <h1 style={{ marginLeft: "50px", color: "white" }}>Log in</h1>
          <Form.Item
            placeholder="Username"
            value={username}
            onChange={(e) => setUsername(e.target.value)}
            rules={[
              {
                required: true,
                message: "Please input your username!",
              },
            ]}
          >
            <Input placeholder="Username" />
          </Form.Item>

          <Form.Item
            name="password"
            value={password}
            onChange={(e) => setPassword(e.target.value)}
            rules={[
              {
                required: true,
                message: "Please input your password!",
              },
            ]}
          >
            <Input.Password placeholder="Password" />
          </Form.Item>

          <Form.Item
            name="remember"
            valuePropName="checked"
            wrapperCol={{
              offset: 8,
              span: 16,
            }}
          >
            {isError && <div className="error">{isError}</div>}

            <Checkbox>Remember me</Checkbox>
          </Form.Item>

          <Form.Item
            wrapperCol={{
              offset: 8,
              span: 16,
            }}
          >
            {/* <Button type="primary" htmlType="submit" onClick={handleOk}>
        Submit
      </Button> */}
          </Form.Item>
        </div>
      </Form>
      {/* </section> */}
    </Modal>
  );
    }
export default LogIn;