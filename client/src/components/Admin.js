import React, { useEffect, useState } from "react";
import dayjs from "dayjs";
import axios from "axios";

import {Select, TimePicker, Button, Checkbox, Form, Input, Space } from "antd";
import FormItem from "antd/es/form/FormItem";

const Admin = () => {
  const [duration, setDuration] = useState("");
  const [name, setName] = useState("");
  const [description, setDescription] = useState("");
  const [familyFriendly, setFamilyFriendly] = useState(false);
  const [longitude, setLongitude] = useState("");
  const [latitude, setLatitude] = useState("");
  const [parking, setParking] = useState(false);
  const [listOfCities, setListOfCities] = useState([]);
  const [pickedCity, setPickedCity] = useState("");
  const [idOfAttractionDelete, setIdOfAttractionDelete] = useState("");

  const [pickedAction, setPickedAction] = useState("");
  const [hashtagName, setHashtagName] = useState("");
  const [hashtagId, setHashtagId] = useState("");

  const [activityName, setActivityName] = useState("");
  const [activityId, setActivityId] = useState("");

  const [cityName, setCityName] = useState("");
  const [cityId, setCityId] = useState("");
  const [cityDescription, setCityDescription] = useState("");

  const [idOfAttractionCHasHashtag, setIdOfAttractionCHasHashtag] =useState("");
  const [idOfHashtafCHasHashtag, setIdOfHashtafCHasHashtag] = useState("");

  const [idOfAttractionDHasHashtag, setIdOfAttractionDHasHashtag] =useState("");
  const [idOfHashtafDHasHashtag, setIdOfHashtafDHasHashtag] = useState("");

  const [idOfAttractionCHasActivity, setIdOfAttractionCHasActivity] =
    useState("");
  const [idOfActivityCHasActivity, setIdOfActivityCHasActivity] = useState("");
  const [durationOfActivity, setDurationOfActivity] = useState("");

  const [idOfAttractionDHasActivity, setIdOfAttractionDHasActivity] =useState("");
  const [idOfHashtafDHasActivity, setIdOfHashtafDHasActivity] = useState("");

  const [idOfAttractionCHasAttraction, setIdOfAttractionCHasAttraction] = useState("");
  const [idOfCityCHasAttraction, setIdOfCityCHasAttraction] = useState("");
  const [idOfAttractionDHasAttraction, setIdOfAttractionDHasAttraction] = useState("");
  const [idOfCityDHasAttraction, setIdOfCityDHasAttraction] = useState("");

  const [experience, setExperience] = useState(false);
  const [minAge, setMinAge] = useState(0);
  const [maxAge, setMaxAge] = useState(0);

  useEffect(() => {
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
  }, []);

  const onFinish = () => {
    console.log("Success:");
    let obj = {};
    console.log(pickedAction);
    if (pickedAction == "addAttraction") {
      obj = {
        name,
        duration,
        description,
        familyFriendly,
        parking,
        longitude,
        latitude,
      };

      axios
        .post(`http://127.0.0.1:5000/admin/createAttraction`, obj, {
          headers: { Authorization: `Bearer ${localStorage.getItem("token")}` },
        })
        .then((responce) => {
          if (responce.status === 200) {
            console.log(responce.data);
            const idOfCityCHasAttraction = pickedCity;
            const idOfAttractionCHasAttraction = responce.data["id"];
            const body = {
              idOfCityCHasAttraction,
              idOfAttractionCHasAttraction,
            };
            axios
              .post(
                `http://127.0.0.1:5000/admin/createRelationship_HAS_ATTRACTION`,
                body,
                {
                  headers: {
                    Authorization: `Bearer ${localStorage.getItem("token")}`,
                  },
                }
              )
              .then((responce) => {
                if (responce.status === 200) {
                  console.log(responce.data);
                //   setName("");
                //   setDuration("");
                //   // setDescription("");
                //   setFamilyFriendly("");
                //   setParking("");
                //   setLongitude("");
                //   setLatitude("");
                 }
                if (responce.status === 206) {
                  console.log(responce.data);
                }
              })
              .catch((error) => {
                console.error("Error:", error);
              });
          }
          if (responce.status === 206) {
            console.log(responce.data);
          }
        })
        .catch((error) => {
          console.error("Error:", error);
        });
    } else if (pickedAction == "deleteAttraction") {
      axios
        .delete(
          `http://127.0.0.1:5000/admin/deleteAttraction/${idOfAttractionDelete}`,
          {
            headers: {
              Authorization: `Bearer ${localStorage.getItem("token")}`,
            },
          }
        )
        .then((responce) => {
          if (responce.status === 200) {
            console.log(responce.data);
            // setIdOfAttractionDelete("")
          }
        })
        .catch((error) => {
          console.error("Error:", error);
        });
    } else if (pickedAction == "addHashtag") {
      const hashName = hashtagName;
      axios
        .post(`http://127.0.0.1:5000/admin/createHashtag/${hashName}`, null, {
          headers: {
            Authorization: `Bearer ${localStorage.getItem("token")}`,
          },
        })
        .then((responce) => {
          if (responce.status === 200) {
            console.log(responce.data);
            // setHashtagName("")
          }
        })
        .catch((error) => {
          console.error("Error:", error);
        });
    } else if (pickedAction == "deleteHashtag") {
      axios
        .delete(`http://127.0.0.1:5000/admin/deleteHashtag/${hashtagId}`, {
          headers: {
            Authorization: `Bearer ${localStorage.getItem("token")}`,
          },
        })
        .then((responce) => {
          if (responce.status === 200) {
            console.log(responce.data);
            // setHashtagId("")
          }
        })
        .catch((error) => {
          console.error("Error:", error);
        });
    } else if (pickedAction == "addActivity") {
      axios
        .post(
          `http://127.0.0.1:5000/admin/createActivity/${activityName}`,
          null,
          {
            headers: {
              Authorization: `Bearer ${localStorage.getItem("token")}`,
            },
          }
        )
        .then((responce) => {
          if (responce.status === 200) {
            console.log(responce.data);
            // setActivityName("")
          }
        })
        .catch((error) => {
          console.error("Error:", error);
        });
    } else if (pickedAction == "deleteActivity") {
      axios
        .delete(`http://127.0.0.1:5000/admin/deleteActivity/${activityId}`, {
          headers: {
            Authorization: `Bearer ${localStorage.getItem("token")}`,
          },
        })
        .then((responce) => {
          if (responce.status === 200) {
            console.log(responce.data);
            // setActivityId("")
          }
        })
        .catch((error) => {
          console.error("Error:", error);
        });
    } else if (pickedAction == "addCity") {
      obj = {
        cityName,
        cityDescription,
      };
      axios
        .post(`http://127.0.0.1:5000/admin/createCity`, obj, {
          headers: {
            Authorization: `Bearer ${localStorage.getItem("token")}`,
          },
        })
        .then((responce) => {
          if (responce.status === 200) {
            console.log(responce.data);
            // setCityName("")
            // setCityDescription("")
          }
        })
        .catch((error) => {
          console.error("Error:", error);
        });
    } else if (pickedAction == "deleteCity") {
      axios
        .delete(`http://127.0.0.1:5000/admin/deleteCity/${cityId}`, {
          headers: {
            Authorization: `Bearer ${localStorage.getItem("token")}`,
          },
        })
        .then((responce) => {
          if (responce.status === 200) {
            console.log(responce.data);
            // setCityId("")
          }
        })
        .catch((error) => {
          console.error("Error:", error);
        });
    } else if (pickedAction == "addHAS_HASHTAG") {
      axios
        .post(
          `http://127.0.0.1:5000/admin/createRelationship_HAS_HASHTAG/${idOfAttractionCHasHashtag}/${idOfHashtafCHasHashtag}`,
          null,
          {
            headers: {
              Authorization: `Bearer ${localStorage.getItem("token")}`,
            },
          }
        )
        .then((responce) => {
          if (responce.status === 200) {
            console.log(responce.data);
            // setIdOfAttractionCHasHashtag("")
            // setIdOfHashtafCHasHashtag("")
          }
        })
        .catch((error) => {
          console.error("Error:", error);
        });
    } else if (pickedAction == "deleteHAS_HASHTAG") {
      axios
        .delete(
          `http://127.0.0.1:5000/admin/deleteRelationship_HAS_HASHTAG/${idOfAttractionDHasHashtag}/${idOfHashtafDHasHashtag}`,
          {
            headers: {
              Authorization: `Bearer ${localStorage.getItem("token")}`,
            },
          }
        )
        .then((responce) => {
          if (responce.status === 200) {
            console.log(responce.data);
            // setIdOfAttractionDHasHashtag("")
            // setIdOfHashtafDHasHashtag("")
          }
          if(responce.status===206){
            console.log(responce.data)
          }
        })
        .catch((error) => {
          console.error("Error:", error);
        });
    } else if (pickedAction == "addHAS_ACTIVITY") {
      obj = {
        idOfAttractionCHasActivity,
        idOfActivityCHasActivity,
        durationOfActivity,
        experience,
        minAge,
        maxAge,
      };
      axios
        .post(
          `http://127.0.0.1:5000/admin/createRelationship_HAS_ACTIVITY`,
          obj,
          {
            headers: {
              Authorization: `Bearer ${localStorage.getItem("token")}`,
            },
          }
        )
        .then((responce) => {
          if (responce.status === 200) {
            console.log(responce.data);
            // setIdOfAttractionCHasActivity("")
            // setIdOfActivityCHasActivity("")
            // setDurationOfActivity("");
            // setExperience("")
            // setMinAge("")
            // setMaxAge("");
          }
          if(responce.status===206)
          {
            console.log(responce.data);

          }
        })
        .catch((error) => {
          console.error("Error:", error);
        });
    } else if (pickedAction == "deleteHAS_ACTIVITY") {
      axios
        .delete(
          `http://127.0.0.1:5000/admin/deleteRelationship_HAS_ACTIVITY/${idOfAttractionDHasActivity}/${idOfHashtafDHasActivity}`,
          {
            headers: {
              Authorization: `Bearer ${localStorage.getItem("token")}`,
            },
          }
        )
        .then((responce) => {
          if (responce.status === 200) {
            console.log(responce.data);
            // setIdOfAttractionDHasActivity("")
            // setIdOfHashtafDHasActivity("")
          }
        })
        .catch((error) => {
          console.error("Error:", error);
        });
    } else if (pickedAction == "addHAS_ATTRACTION") {
      obj = {
        idOfAttractionCHasAttraction,
        idOfCityCHasAttraction,
      };
      axios
        .post(
          `http://127.0.0.1:5000/admin/createRelationship_HAS_ATTRACTION`,
          obj,
          {
            headers: {
              Authorization: `Bearer ${localStorage.getItem("token")}`,
            },
          }
        )
        .then((responce) => {
          if (responce.status === 200) {
            console.log(responce.data);
            // setIdOfAttractionCHasAttraction("")
            // setIdOfCityCHasAttraction("")

          }
        })
        .catch((error) => {
          console.error("Error:", error);
        });
    } else if (pickedAction == "deleteHAS_ATTRACTION") {
      axios
        .delete(
          `http://127.0.0.1:5000/admin/deleteRelationship_HAS_ATTRACTION/${idOfCityDHasAttraction}/${idOfAttractionDHasAttraction}`,
          {
            headers: {
              Authorization: `Bearer ${localStorage.getItem("token")}`,
            },
          }
        )
        .then((responce) => {
          if (responce.status === 200) {
            console.log(responce.data);
            // setIdOfCityDHasAttraction("")
            // setIdOfAttractionDHasAttraction("")

          }
        })
        .catch((error) => {
          console.error("Error:", error);
        });
    }
  };
  const onFinishFailed = (errorInfo) => {
    console.log("Failed:", errorInfo);
  };
  const onChangeTime = (time, timeString) => {
    console.log(time);
    console.log(timeString);
    setDuration(timeString);
  };
  const onChangeTimeActivity = (time, timeString) => {
    console.log(time);
    console.log(timeString);
    setDurationOfActivity(timeString);
  };
  const onChangeCity = (value) => {
    setPickedCity(value);
  };
  const onSearch = (value) => {
    console.log("search:", value);
  };

  const filterOption = (input, option) =>
    (option?.label ?? "").toLowerCase().includes(input.toLowerCase());

  return (
    <>
      <>
        <Space
          direction="vertical"
          size="middle"
          style={{
            display: "flex",
          }}
        >
          <Form
            name="basic"
            labelCol={{
              span: 8,
            }}
            wrapperCol={{
              span: 16,
            }}
            style={{
              maxWidth: 600,
            }}
            initialValues={{
              remember: true,
            }}
            onFinish={() => {
              onFinish();
            }}
            onFinishFailed={onFinishFailed}
            autoComplete="off"
          >
            <h1>Attraction</h1>
            <Space
              direction="vertical"
              size="middle"
              style={{
                display: "flex",
              }}
            >
              <Form.Item>
                <h2>Add attraction</h2>
              </Form.Item>

              <Form.Item
                label="Name"
                name="name"
                value={name}
                onChange={(e) => setName(e.target.value)}
                rules={[
                  {
                    required: true,
                    message: "Please input name!",
                  },
                ]}
              >
                <Input />
              </Form.Item>

              <Form.Item
                label="Description"
                name="description"
                value={description}
                onChange={(e) => setDescription(e.target.value)}
                rules={[
                  {
                    required: true,
                    message: "Please input description!",
                  },
                ]}
              >
                <Input />
              </Form.Item>
              <Form.Item
                label="Longitude"
                name="longitude"
                value={longitude}
                onChange={(e) => setLongitude(e.target.value)}
                rules={[
                  {
                    required: true,
                    message: "Please input longitude!",
                  },
                ]}
              >
                <Input type="number" />
              </Form.Item>
              <Form.Item
                label="Latitude"
                name="latitude"
                value={latitude}
                onChange={(e) => setLatitude(e.target.value)}
                rules={[
                  {
                    required: true,
                    message: "Please input latitude!",
                  },
                ]}
              >
                <Input type="number" />
              </Form.Item>
              <Form.Item
                label="Duration of visit"
                name="duration_of_visit"
                value={duration}
                onChange={(e) => setDuration(e.target.value)}
                rules={[
                  {
                    required: true,
                    message: "Please input average duration of visit!",
                  },
                ]}
              >
                <TimePicker
                  style={{ marginBottom: "8px" }}
                  onChange={onChangeTime}
                  defaultOpenValue={dayjs("00:00:00", "HH:mm:ss")}
                />
              </Form.Item>
              <Form.Item label="Parking" name="parking" value={parking}>
                <Checkbox
                  onChange={(e) => setParking(e.target.checked)}
                ></Checkbox>
              </Form.Item>

              <Form.Item
                label="Family friendly"
                name="family_friendly"
                value={familyFriendly}
              >
                <Checkbox
                  onChange={(e) => setFamilyFriendly(e.target.checked)}
                ></Checkbox>
              </Form.Item>
              <Form.Item
                label="City"
                name="city"
                rules={[
                  {
                    required: true,
                    message: "Please input description!",
                  },
                ]}
              >
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
              </Form.Item>

              <Form.Item
                wrapperCol={{
                  offset: 8,
                  span: 16,
                }}
              >
                <Button
                  onClick={() => {
                    setPickedAction("addAttraction");
                  }}
                  type="primary"
                  htmlType="submit"
                >
                  Submit
                </Button>
              </Form.Item>
            </Space>
          </Form>

          <Form
            name="basic"
            labelCol={{
              span: 8,
            }}
            wrapperCol={{
              span: 16,
            }}
            style={{
              maxWidth: 600,
            }}
            initialValues={{
              remember: true,
            }}
            onFinish={() => {
              onFinish();
            }}
            onFinishFailed={onFinishFailed}
            autoComplete="off"
          >
            <Form.Item>
              <h2>Delete attraction</h2>
            </Form.Item>

            <Form.Item
              label="Id of attraction"
              name="idOfAttraction"
              value={idOfAttractionDelete}
              onChange={(e) => setIdOfAttractionDelete(e.target.value)}
              rules={[
                {
                  required: true,
                  message: "Please input id!",
                },
              ]}
            >
              <Input />
            </Form.Item>
            <Form.Item
              wrapperCol={{
                offset: 8,
                span: 16,
              }}
            >
              <Button
                onClick={() => {
                  setPickedAction("deleteAttraction");
                }}
                type="primary"
                htmlType="submit"
              >
                Submit
              </Button>
            </Form.Item>
          </Form>
        </Space>

        <Space
          direction="vertical"
          size="middle"
          style={{
            display: "flex",
          }}
        >
          <Form
            name="basic"
            labelCol={{
              span: 8,
            }}
            wrapperCol={{
              span: 16,
            }}
            style={{
              maxWidth: 600,
            }}
            initialValues={{
              remember: true,
            }}
            onFinish={() => {
              onFinish();
            }}
            onFinishFailed={onFinishFailed}
            autoComplete="off"
          >
            <h1>Hashtag</h1>
            <Form.Item>
              <h2>Add hashtag</h2>
            </Form.Item>

            <Form.Item
              label="Name"
              name="hashname"
              value={hashtagName}
              onChange={(e) => setHashtagName(e.target.value)}
              rules={[
                {
                  required: true,
                  message: "Please input name!",
                },
              ]}
            >
              <Input />
            </Form.Item>
            <Form.Item
              wrapperCol={{
                offset: 8,
                span: 16,
              }}
            >
              <Button
                onClick={() => {
                  setPickedAction("addHashtag");
                }}
                type="primary"
                htmlType="submit"
              >
                Submit
              </Button>
            </Form.Item>
          </Form>
        </Space>

        <Space
          direction="vertical"
          size="middle"
          style={{
            display: "flex",
          }}
        >
          <Form
            name="basic"
            labelCol={{
              span: 8,
            }}
            wrapperCol={{
              span: 16,
            }}
            style={{
              maxWidth: 600,
            }}
            initialValues={{
              remember: true,
            }}
            onFinish={() => {
              onFinish();
            }}
            onFinishFailed={onFinishFailed}
            autoComplete="off"
          >
            <Form.Item>
              <h2>Delete hashtag</h2>
            </Form.Item>

            <Form.Item
              label="Id of hashtag"
              name="idOfHashtag"
              value={hashtagId}
              onChange={(e) => setHashtagId(e.target.value)}
              rules={[
                {
                  required: true,
                  message: "Please input id!",
                },
              ]}
            >
              <Input />
            </Form.Item>
            <Form.Item
              wrapperCol={{
                offset: 8,
                span: 16,
              }}
            >
              <Button
                onClick={() => {
                  setPickedAction("deleteHashtag");
                }}
                type="primary"
                htmlType="submit"
              >
                Submit
              </Button>
            </Form.Item>
          </Form>
        </Space>

        <Space
          direction="vertical"
          size="middle"
          style={{
            display: "flex",
          }}
        >
          <Form
            name="basic"
            labelCol={{
              span: 8,
            }}
            wrapperCol={{
              span: 16,
            }}
            style={{
              maxWidth: 600,
            }}
            initialValues={{
              remember: true,
            }}
            onFinish={() => {
              onFinish();
            }}
            onFinishFailed={onFinishFailed}
            autoComplete="off"
          >
            <h1>Activity</h1>
            <Form.Item>
              <h2>Add activity</h2>
            </Form.Item>

            <Form.Item
              label="Name"
              name="name"
              value={activityName}
              onChange={(e) => setActivityName(e.target.value)}
              rules={[
                {
                  required: true,
                  message: "Please input name!",
                },
              ]}
            >
              <Input />
            </Form.Item>

            <Form.Item
              wrapperCol={{
                offset: 8,
                span: 16,
              }}
            >
              <Button
                onClick={() => {
                  setPickedAction("addActivity");
                }}
                type="primary"
                htmlType="submit"
              >
                Submit
              </Button>
            </Form.Item>
          </Form>
        </Space>

        <Space
          direction="vertical"
          size="middle"
          style={{
            display: "flex",
          }}
        >
          <Form
            name="basic"
            labelCol={{
              span: 8,
            }}
            wrapperCol={{
              span: 16,
            }}
            style={{
              maxWidth: 600,
            }}
            initialValues={{
              remember: true,
            }}
            onFinish={() => {
              onFinish();
            }}
            onFinishFailed={onFinishFailed}
            autoComplete="off"
          >
            <Form.Item>
              <h2>Delete activity</h2>
            </Form.Item>

            <Form.Item
              label="Id of activity"
              name="idOfActivity"
              value={activityId}
              onChange={(e) => setActivityId(e.target.value)}
              rules={[
                {
                  required: true,
                  message: "Please input id!",
                },
              ]}
            >
              <Input />
            </Form.Item>
            <Form.Item
              wrapperCol={{
                offset: 8,
                span: 16,
              }}
            >
              <Button
                onClick={() => {
                  setPickedAction("deleteActivity");
                }}
                type="primary"
                htmlType="submit"
              >
                Submit
              </Button>
            </Form.Item>
          </Form>
        </Space>

        <Space
          direction="vertical"
          size="middle"
          style={{
            display: "flex",
          }}
        >
          <Form
            name="basic"
            labelCol={{
              span: 8,
            }}
            wrapperCol={{
              span: 16,
            }}
            style={{
              maxWidth: 600,
            }}
            initialValues={{
              remember: true,
            }}
            onFinish={() => {
              onFinish();
            }}
            onFinishFailed={onFinishFailed}
            autoComplete="off"
          >
            <h1>City</h1>
            <Form.Item>
              <h2>Add city</h2>
            </Form.Item>

            <Form.Item
              label="Name"
              name="name"
              value={cityName}
              onChange={(e) => setCityName(e.target.value)}
              rules={[
                {
                  required: true,
                  message: "Please input name!",
                },
              ]}
            >
              <Input />
            </Form.Item>
            <Form.Item
              label="Description"
              name="description"
              value={cityDescription}
              onChange={(e) => setCityDescription(e.target.value)}
              rules={[
                {
                  required: true,
                  message: "Please input name!",
                },
              ]}
            >
              <Input />
            </Form.Item>

            <Form.Item
              wrapperCol={{
                offset: 8,
                span: 16,
              }}
            >
              <Button
                onClick={() => {
                  setPickedAction("addCity");
                }}
                type="primary"
                htmlType="submit"
              >
                Submit
              </Button>
            </Form.Item>
          </Form>
        </Space>

        <Space
          direction="vertical"
          size="middle"
          style={{
            display: "flex",
          }}
        >
          <Form
            name="basic"
            labelCol={{
              span: 8,
            }}
            wrapperCol={{
              span: 16,
            }}
            style={{
              maxWidth: 600,
            }}
            initialValues={{
              remember: true,
            }}
            onFinish={() => {
              onFinish();
            }}
            onFinishFailed={onFinishFailed}
            autoComplete="off"
          >
            <Form.Item>
              <h2>Delete city</h2>
            </Form.Item>

            <Form.Item
              label="Id of city"
              name="id"
              value={cityId}
              onChange={(e) => setCityId(e.target.value)}
              rules={[
                {
                  required: true,
                  message: "Please input id!",
                },
              ]}
            >
              <Input />
            </Form.Item>
            <Form.Item
              wrapperCol={{
                offset: 8,
                span: 16,
              }}
            >
              <Button
                onClick={() => {
                  setPickedAction("deleteCity");
                }}
                type="primary"
                htmlType="submit"
              >
                Submit
              </Button>
            </Form.Item>
          </Form>
        </Space>
      </>

      <>
        <Space
          direction="vertical"
          size="middle"
          style={{
            display: "flex",
          }}
        >
          <Form
            name="basic"
            labelCol={{
              span: 8,
            }}
            wrapperCol={{
              span: 16,
            }}
            style={{
              maxWidth: 600,
            }}
            initialValues={{
              remember: true,
            }}
            onFinish={() => {
              onFinish();
            }}
            onFinishFailed={onFinishFailed}
            autoComplete="off"
          >
            <h1>HAS_HASHTAG relationship</h1>
            <Form.Item>
              <h2>Add relationship</h2>
            </Form.Item>

            <Form.Item
              label="Id of attraction"
              name="idOfAttraction"
              value={idOfAttractionCHasHashtag}
              onChange={(e) => setIdOfAttractionCHasHashtag(e.target.value)}
              rules={[
                {
                  required: true,
                  message: "Please input id!",
                },
              ]}
            >
              <Input />
            </Form.Item>

            <Form.Item
              label="Id of hashtag"
              name="idOfHashtag"
              value={idOfHashtafCHasHashtag}
              onChange={(e) => setIdOfHashtafCHasHashtag(e.target.value)}
              rules={[
                {
                  required: true,
                  message: "Please input id!",
                },
              ]}
            >
              <Input />
            </Form.Item>
            <Form.Item
              wrapperCol={{
                offset: 8,
                span: 16,
              }}
            >
              <Button
                onClick={() => {
                  setPickedAction("addHAS_HASHTAG");
                }}
                type="primary"
                htmlType="submit"
              >
                Submit
              </Button>
            </Form.Item>
          </Form>
        </Space>

        <Space
          direction="vertical"
          size="middle"
          style={{
            display: "flex",
          }}
        >
          <Form
            name="basic"
            labelCol={{
              span: 8,
            }}
            wrapperCol={{
              span: 16,
            }}
            style={{
              maxWidth: 600,
            }}
            initialValues={{
              remember: true,
            }}
            onFinish={() => {
              onFinish();
            }}
            onFinishFailed={onFinishFailed}
            autoComplete="off"
          >
            <Form.Item>
              <h2>Delete relationship</h2>
            </Form.Item>

            <Form.Item
              label="Id of attraction"
              name="idOfAttraction"
              value={idOfAttractionDHasHashtag}
              onChange={(e) => setIdOfAttractionDHasHashtag(e.target.value)}
              rules={[
                {
                  required: true,
                  message: "Please input id!",
                },
              ]}
            >
              <Input />
            </Form.Item>

            <Form.Item
              label="Id of hashtag"
              name="idOfHashtag"
              value={idOfHashtafDHasHashtag}
              onChange={(e) => setIdOfHashtafDHasHashtag(e.target.value)}
              rules={[
                {
                  required: true,
                  message: "Please input id!",
                },
              ]}
            >
              <Input />
            </Form.Item>
            <Form.Item
              wrapperCol={{
                offset: 8,
                span: 16,
              }}
            >
              <Button
                onClick={() => {
                  setPickedAction("deleteHAS_HASHTAG");
                }}
                type="primary"
                htmlType="submit"
              >
                Submit
              </Button>
            </Form.Item>
          </Form>
        </Space>

        <Space
          direction="vertical"
          size="middle"
          style={{
            display: "flex",
          }}
        >
          <Form
            name="basic"
            labelCol={{
              span: 8,
            }}
            wrapperCol={{
              span: 16,
            }}
            style={{
              maxWidth: 600,
            }}
            initialValues={{
              remember: true,
            }}
            onFinish={() => {
              onFinish();
            }}
            onFinishFailed={onFinishFailed}
            autoComplete="off"
          >
            <h1>HAS_ACTIVITY relationship</h1>
            <Form.Item>
              <h2>Add relationship</h2>
            </Form.Item>

            <Form.Item
              label="Id of attraction"
              name="idOfAttraction"
              value={idOfAttractionCHasActivity}
              onChange={(e) => setIdOfAttractionCHasActivity(e.target.value)}
              rules={[
                {
                  required: true,
                  message: "Please input id!",
                },
              ]}
            >
              <Input />
            </Form.Item>

            <Form.Item
              label="Id of activity"
              name="idOfActivity"
              value={idOfActivityCHasActivity}
              onChange={(e) => setIdOfActivityCHasActivity(e.target.value)}
              rules={[
                {
                  required: true,
                  message: "Please input id!",
                },
              ]}
            >
              <Input />
            </Form.Item>
            <Form.Item
              label="Duration of activity"
              name="durationOfActivity"
              value={durationOfActivity}
              onChange={(e) => setDurationOfActivity(e.target.value)}
              rules={[
                {
                  required: true,
                  message: "Please input average duration of activity!",
                },
              ]}
            >
              <TimePicker
                style={{ marginBottom: "8px" }}
                onChange={onChangeTimeActivity}
                defaultOpenValue={dayjs("00:00:00", "HH:mm:ss")}
              />
            </Form.Item>
            <Form.Item label="Experience" name="experience" value={experience}>
              <Checkbox
                onChange={(e) => setExperience(e.target.checked)}
              ></Checkbox>
            </Form.Item>
            <Form.Item
              label="Min age"
              name="minAge"
              value={minAge}
              onChange={(e) => setMinAge(e.target.value)}
              rules={[
                {
                  required: true,
                  message: "Please input age!",
                },
              ]}
            >
              <Input type="number" />
            </Form.Item>
            <Form.Item
              label="Max age"
              name="maxAge"
              value={maxAge}
              onChange={(e) => setMaxAge(e.target.value)}
              rules={[
                {
                  required: true,
                  message: "Please input age!",
                },
              ]}
            >
              <Input type="number" />
            </Form.Item>

            <Form.Item
              wrapperCol={{
                offset: 8,
                span: 16,
              }}
            >
              <Button
                onClick={() => {
                  setPickedAction("addHAS_ACTIVITY");
                }}
                type="primary"
                htmlType="submit"
              >
                Submit
              </Button>
            </Form.Item>
          </Form>
        </Space>

        <Space
          direction="vertical"
          size="middle"
          style={{
            display: "flex",
          }}
        >
          <Form
            name="basic"
            labelCol={{
              span: 8,
            }}
            wrapperCol={{
              span: 16,
            }}
            style={{
              maxWidth: 600,
            }}
            initialValues={{
              remember: true,
            }}
            onFinish={() => {
              onFinish();
            }}
            onFinishFailed={onFinishFailed}
            autoComplete="off"
          >
            <Form.Item>
              <h2>Delete relationship</h2>
            </Form.Item>

            <Form.Item
              label="Id of attraction"
              name="idOfAttraction"
              value={idOfAttractionDHasActivity}
              onChange={(e) => setIdOfAttractionDHasActivity(e.target.value)}
              rules={[
                {
                  required: true,
                  message: "Please input id!",
                },
              ]}
            >
              <Input />
            </Form.Item>

            <Form.Item
              label="Id of activity"
              name="idOfActivity"
              value={idOfHashtafDHasActivity}
              onChange={(e) => setIdOfHashtafDHasActivity(e.target.value)}
              rules={[
                {
                  required: true,
                  message: "Please input id!",
                },
              ]}
            >
              <Input />
            </Form.Item>
            <Form.Item
              wrapperCol={{
                offset: 8,
                span: 16,
              }}
            >
              <Button
                onClick={() => {
                  setPickedAction("deleteHAS_ACTIVITY");
                }}
                type="primary"
                htmlType="submit"
              >
                Submit
              </Button>
            </Form.Item>
          </Form>
        </Space>

        <Space
          direction="vertical"
          size="middle"
          style={{
            display: "flex",
          }}
        >
          <Form
            name="basic"
            labelCol={{
              span: 8,
            }}
            wrapperCol={{
              span: 16,
            }}
            style={{
              maxWidth: 600,
            }}
            initialValues={{
              remember: true,
            }}
            onFinish={() => {
              onFinish();
            }}
            onFinishFailed={onFinishFailed}
            autoComplete="off"
          >
            <h1>HAS_ATTRACTION relationship</h1>
            <Form.Item>
              <h2>Add relationship</h2>
            </Form.Item>

            <Form.Item
              label="Id of attraction"
              name="idOfAttraction"
              value={idOfAttractionCHasAttraction}
              onChange={(e) => setIdOfAttractionCHasAttraction(e.target.value)}
              rules={[
                {
                  required: true,
                  message: "Please input id!",
                },
              ]}
            >
              <Input />
            </Form.Item>

            <Form.Item
              label="Id of city"
              name="idOfCity"
              value={idOfCityCHasAttraction}
              onChange={(e) => setIdOfCityCHasAttraction(e.target.value)}
              rules={[
                {
                  required: true,
                  message: "Please input id!",
                },
              ]}
            >
              <Input />
            </Form.Item>
            <Form.Item
              wrapperCol={{
                offset: 8,
                span: 16,
              }}
            >
              <Button
                onClick={() => {
                  setPickedAction("addHAS_ATTRACTION");
                }}
                type="primary"
                htmlType="submit"
              >
                Submit
              </Button>
            </Form.Item>
          </Form>
        </Space>

        <Space
          direction="vertical"
          size="middle"
          style={{
            display: "flex",
          }}
        >
          <Form
            name="basic"
            labelCol={{
              span: 8,
            }}
            wrapperCol={{
              span: 16,
            }}
            style={{
              maxWidth: 600,
            }}
            initialValues={{
              remember: true,
            }}
            onFinish={() => {
              onFinish();
            }}
            onFinishFailed={onFinishFailed}
            autoComplete="off"
          >
            <Form.Item>
              <h2>Delete relationship</h2>
            </Form.Item>

            <Form.Item
              label="Id of attraction"
              name="idOfAttraction"
              value={idOfAttractionDHasAttraction}
              onChange={(e) => setIdOfAttractionDHasAttraction(e.target.value)}
              rules={[
                {
                  required: true,
                  message: "Please input id!",
                },
              ]}
            >
              <Input />
            </Form.Item>

            <Form.Item
              label="Id of city"
              name="idOfCity"
              value={idOfCityDHasAttraction}
              onChange={(e) => setIdOfCityDHasAttraction(e.target.value)}
              rules={[
                {
                  required: true,
                  message: "Please input id!",
                },
              ]}
            >
              <Input />
            </Form.Item>
            <Form.Item
              wrapperCol={{
                offset: 8,
                span: 16,
              }}
            >
              <Button
                onClick={() => {
                  setPickedAction("deleteHAS_ATTRACTION");
                }}
                type="primary"
                htmlType="submit"
              >
                Submit
              </Button>
            </Form.Item>
          </Form>
        </Space>
      </>
      <Alert message="Error Text" type="error" />
    </>
  );
};
export default Admin;
