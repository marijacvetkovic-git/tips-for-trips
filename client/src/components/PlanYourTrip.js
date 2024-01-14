import React, { useState } from "react";
import { useNavigate } from "react-router-dom";

import axios from "axios";
import {
  TimePicker,
  Select,
  Button,
  Checkbox,
  Form,
  Input,
  List,
  Space,
} from "antd";
import { LikeOutlined, MessageOutlined, StarOutlined } from "@ant-design/icons";
import dayjs from "dayjs";
import customParseFormat from "dayjs/plugin/customParseFormat";
import { getUserId } from "../utils";
import Item from "antd/es/list/Item";
dayjs.extend(customParseFormat);

const PlanYourTrip = () => {
  const [longitude, setLongitude] = useState("");
  const [latitude, setLatitude] = useState("");
  const [listOfCities, setListOfCities] = useState([]);
  const [listOfActivities, setListOfActivities] = useState([]);
  const [pickedCity, setPickedCity] = useState("");
  const [pickedActivities, setPickedActivities] = useState([]);
  const [pickedDuration, setPickedDuration] = useState("");
  const [pickedKms, setpickedKms] = useState("");
  const [parking, setParking] = useState(false);
  const [familyFriendly, setFamilyFriendly] = useState(false);
  const [maxDestinations, setMaxDestinations] = useState("");
  const [listOfAttractions, setListOfAttractions] = useState([]);
  const userId = getUserId();
  const navigate = useNavigate();

  const onChange = (value) => {
    console.log(`selected ${value}`);
    setPickedDuration(value);
  };
  const onChangeCity = (value) => {
    setPickedCity(value);
  };
  const onSearch = (value) => {
    console.log("search:", value);
  };

  const filterOption = (input, option) =>
    (option?.label ?? "").toLowerCase().includes(input.toLowerCase());

  const onChangeTime = (time, timeString) => {
    console.log(time);
    console.log(timeString);
    setPickedDuration(timeString);
  };

  const handleOk = () => {
    let pickedAct = "";
    let maxDest = -1;
    let pickedKm = 0;
    if (pickedKms != "") pickedKm = pickedKms;
    if (pickedActivities != []) pickedAct = pickedActivities.join(",");
    if (maxDestinations == "") maxDest = 0;
    else maxDest = maxDestinations;
    const planBody = {
      pickedDuration,
      pickedAct,
      pickedCity,
      pickedKm,
      parking,
      familyFriendly,
      maxDest,
      latitude,
      longitude,
    };
    console.log(planBody);
    axios
      .post(`http://127.0.0.1:5000/user/planTrip`, planBody, {
        headers: { Authorization: `Bearer ${localStorage.getItem("token")}` },
      })
      .then((responce) => {
        if (responce.status === 200) {
          console.log(responce.data);
          setListOfAttractions(responce.data);
        }
      })
      .catch((error) => {
        console.error("Error:", error);
      });
  };

  const data = listOfAttractions.map((attraction, i) => ({
    href: "/home",
    title: attraction["name"],
    content: `Total duration with matched activities ${attraction["houres"]}:${attraction["minutes"]}:${attraction["seconds"]} 
  Number of matched activities ${attraction["matchedActivities"]} 
  Distance in km ${attraction["distaneInKm"]}`,
    id: attraction["id"],
    avgRate: attraction["avgRate"],
    image:attraction["image"]
  }));

  const IconText = ({ icon, text }) => (
    <Space>
      {React.createElement(icon)}
      {text}
    </Space>
  );
  useState(() => {
    axios
      .get(`http://127.0.0.1:5000/helpers/getLongitudeLatitude/${userId}`)
      .then((responce) => {
        if (responce.status === 200) {
          console.log(responce.data);
          setLatitude(responce.data[0]["latitude"]);
          setLongitude(responce.data[0]["longitude"]);
        }
      })
      .catch((error) => {
        console.error("Error:", error);
      });

    axios
      .get("http://127.0.0.1:5000/helpers/getCities")
      .then((responce) => {
        if (responce.status === 200) {
          console.log(responce.data);
          setListOfCities(responce.data);
        }
      })
      .catch((error) => {
        console.error("Error:", error);
      });

    axios
      .get("http://127.0.0.1:5000/helpers/getActivities")
      .then((responce) => {
        if (responce.status === 200) {
          console.log(responce.data);
          setListOfActivities(responce.data);
        }
      })
      .catch((error) => {
        console.error("Error:", error);
      });
  }, []);

  return (
    <>
      <>
        <Form
          labelCol={{ span: 8 }}
          wrapperCol={{ span: 16 }}
          style={{ maxWidth: 600 }}
          onFinish={handleOk}
        >
          <h2>Plan your trip</h2>
          <Select
            showSearch
            style={{ marginBottom: "8px" }}
            placeholder="Select a city"
            optionFilterProp="children"
            onChange={onChangeCity}
            onSearch={onSearch}
            filterOption={filterOption}
            rules={[
              {
                required: true,
                message: "Please select some city",
              },
            ]}
            options={listOfCities.map((item) => ({
              value: item["id"],
              label: item["name"],
            }))}
          />
          <Input
            value={pickedKms}
            style={{ marginBottom: "8px" }}
            type="number"
            size="small"
            placeholder="Distanced from your location"
            suffix="km"
            onChange={(e) => setpickedKms(e.target.value)}
          />
          <Select
            mode="multiple"
            placeholder="Select activities"
            value={pickedActivities}
            onChange={(value) => setPickedActivities(value)}
            style={{
              width: "100%",
              marginBottom: "8px",
            }}
            options={listOfActivities.map((item) => ({
              value: item["id"],
              label: item["name"],
            }))}
          />
          <TimePicker
            style={{ marginBottom: "8px" }}
            onChange={onChangeTime}
            defaultOpenValue={dayjs("00:00:00", "HH:mm:ss")}
          />
          <div>
            <Checkbox
              onChange={(e) => {
                setParking(e.target.checked);
              }}
              style={{ marginBottom: "8px" }}
            >
              Parking
            </Checkbox>
          </div>

          <div>
            <Checkbox
              onChange={(e) => {
                setFamilyFriendly(e.target.checked);
              }}
              style={{ marginBottom: "8px" }}
            >
              Family friendly
            </Checkbox>
          </div>

          <Input
            value={maxDestinations}
            style={{ marginBottom: "8px" }}
            type="number"
            placeholder="Max destinations, default 5"
            onChange={(e) => setMaxDestinations(e.target.value)}
          />
          <Button type="primary" htmlType="submit">
            Plan
          </Button>
        </Form>
      </>

      <>
        <List
          itemLayout="vertical"
          size="large"
          dataSource={data}
          renderItem={(item) => (
            <List.Item
              key={item.title}
              actions={[
                <IconText
                  icon={StarOutlined}
                  text={item.avgRate}
                  key="list-vertical-star-o"
                />,
                // <IconText
                //   icon={LikeOutlined}
                //   text="156"
                //   key="list-vertical-like-o"
                // />,
                // <IconText
                //   icon={MessageOutlined}
                //   text="2"
                //   key="list-vertical-message"
                // />,
              ]}
              extra={
                <img
                  width={272}
                  alt="logo"
                  src={item.image}
                  style={{
                    display: "block",
                    width: "20vw",
                    height: "30vh",
                    // Postavite širinu na 100%
                  }}
                />
              }
            >
              <List.Item.Meta
                title={
                  <a
                    onClick={() => navigate("/attraction", { state: item.id })}
                    style={{ cursor: "pointer" }}
                  >
                    {item.title}
                  </a>
                }
                // description={item.description}
              />
              {item.content}
            </List.Item>
          )}
        />
      </>
    </>
  );
};
export default PlanYourTrip;
