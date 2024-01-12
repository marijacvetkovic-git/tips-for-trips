import React, { useState,useEffect } from "react";
import { List, Col, Divider, Drawer, Row } from "antd";
import axios from "axios";
import { getUserId } from "../utils";
import { UserOutlined } from "@ant-design/icons";
import { Avatar } from "antd";

const Profile = () => {
  const [open, setOpen] = useState(true);
  const [attractionInfo,setAttractionInfo]=useState("")

  const onClose = () => {
    setOpen(false);
    window.location="/home"
  };
  const DescriptionItem = ({ title, content }) => (
    <div className="site-description-item-profile-wrapper">
      <p className="site-description-item-profile-p-label">
        {title}: {content}
      </p>
    </div>
  );
  
  useEffect(()=>{
    axios
      .get(`http://127.0.0.1:5000/helpers/getUser/${getUserId()}`)
      .then((responce) => {
        if (responce.status == 200) {
        setAttractionInfo(responce.data[0]);
        console.log(responce.data)}
      })
      .catch((error) => {
        console.error("Error:", error);
      });

  },[])
  return (
    <>
      <Drawer placement="right" onClose={onClose} open={open}>
        <Avatar
          style={{
            backgroundColor: "#87d068",
          }}
          icon={<UserOutlined />}
        />
        <p
          className="site-description-item-profile-p"
          style={{
            display: "flex",
          }}
        >
          Your Profile
        </p>
        <Row>
          <DescriptionItem
            title="Username"
            content={attractionInfo["username"]}
          />
        </Row>
        <Row>
          <DescriptionItem title="Email" content={attractionInfo["email"]} />
        </Row>
        <Row>
          <DescriptionItem
            title="Date of birth"
            content={attractionInfo["date"]}
          />
        </Row>
        {attractionInfo && (
          <>
            {" "}
            {attractionInfo["attractionNames"].length != 0 && (
              <>
                <Divider />
                <p className="site-description-item-profile-p">
                  Visited attractions
                </p>
                <List
                  bordered
                  dataSource={attractionInfo["attractionNames"]}
                  renderItem={(item) => <List.Item>{item}</List.Item>}
                />
                <Divider />
              </>
            )}
          </>
        )}

        <Row
          gutter={{
            xs: 8,
            sm: 16,
            md: 24,
            lg: 32,
          }}
          style={{ marginTop: "10px" }}
        >
          {attractionInfo &&
            attractionInfo["hashtags"].map((item) => (
              <Col>
                <a key={item} style={{ cursor: "pointer" }}>
                  #{item}
                </a>
              </Col>
            ))}
        </Row>
      </Drawer>
    </>
  );
};
export default Profile;
