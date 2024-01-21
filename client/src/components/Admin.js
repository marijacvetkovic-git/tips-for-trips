import React, { useEffect, useState } from "react";
import dayjs from "dayjs";
import axios from "axios";

import { Select, TimePicker, Button, Checkbox, Form, Input, Space, message, Upload } from "antd";
import { UploadOutlined } from "@ant-design/icons";
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
  const [idOfAttractionDeleteError, setIdOfAttractionDeleteError] = useState("");

  const [nameError, setNameError] = useState("");
  const [latitudeError, setLatitudeError] = useState("");

  const [pickedAction, setPickedAction] = useState("");
  const [hashtagName, setHashtagName] = useState("");

  const [hashtagNameError, setHashtagNameError] = useState("");

  const [hashtagId, setHashtagId] = useState("");
  const [hashtagIdError, setHashtagIdError] = useState("");


  const [activityName, setActivityName] = useState("");
  const [activityNameError, setActivityNameError] = useState("");

  const [activityId, setActivityId] = useState("");
  const [activityIdError, setActivityIdError] = useState("");

  const [cityName, setCityName] = useState("");
  const [cityNameError, setCityNameError] = useState("");

  const [cityId, setCityId] = useState("");
  const [cityIdError, setCityIdError] = useState("");

  const [cityDescription, setCityDescription] = useState("");

  const [idOfAttractionCHasHashtag, setIdOfAttractionCHasHashtag] =
    useState("");
    const [idOfAttractionCHasHashtagError, setIdOfAttractionCHasHashtagError] =
      useState("");
      
  const [idOfHashtafCHasHashtag, setIdOfHashtafCHasHashtag] = useState("");
    const [idOfHashtafCHasHashtagError, setIdOfHashtafCHasHashtagError] = useState("");


  const [idOfAttractionDHasHashtag, setIdOfAttractionDHasHashtag] =
    useState("");
  const [idOfHashtafDHasHashtag, setIdOfHashtafDHasHashtag] = useState("");
  

    const [idOfAttractionDHasHashtagError, setIdOfAttractionDHasHashtagError] =
      useState("");
    const [idOfHashtafDHasHashtagError, setIdOfHashtafDHasHashtagError] = useState("");


  const [idOfAttractionCHasActivity, setIdOfAttractionCHasActivity] =
    useState("");
  const [idOfActivityCHasActivity, setIdOfActivityCHasActivity] = useState("");
    const [idOfAttractionCHasActivityError, setIdOfAttractionCHasActivityError] =
      useState("");
    const [idOfActivityCHasActivityError, setIdOfActivityCHasActivityError] =
      useState("");
  const [durationOfActivity, setDurationOfActivity] = useState("");

  const [idOfAttractionDHasActivity, setIdOfAttractionDHasActivity] =
    useState("");
  const [idOfActivityDHasActivity, setIdOfActivityDHasActivity] = useState("");

    const [idOfAttractionDHasActivityError, setIdOfAttractionDHasActivityError] =
    useState("");
  const [idOfActivityDHasActivityError, setIdOfActivityDHasActivityError] = useState("");

  const [idOfAttractionCHasAttraction, setIdOfAttractionCHasAttraction] =
    useState("");
  const [idOfCityCHasAttraction, setIdOfCityCHasAttraction] = useState("");
 const [idOfAttractionCHasAttractionError, setIdOfAttractionCHasAttractionError] =
   useState("");
 const [idOfCityCHasAttractionError, setIdOfCityCHasAttractionError] = useState("");


  const [idOfAttractionDHasAttraction, setIdOfAttractionDHasAttraction] =
    useState("");
  const [idOfCityDHasAttraction, setIdOfCityDHasAttraction] = useState("");

    const [idOfAttractionDHasAttractionError, setIdOfAttractionDHasAttractionError] =
      useState("");
    const [idOfCityDHasAttractionError, setIdOfCityDHasAttractionError] = useState("");

  const [experience, setExperience] = useState(false);
  const [minAge, setMinAge] = useState(0);
  const [maxAge, setMaxAge] = useState(0);



  const cleanErrors = () => {
    setIdOfAttractionDeleteError("")
    setLatitudeError("")
    setHashtagNameError("")
    setHashtagIdError("")
    setActivityNameError("")
    setActivityIdError("")
    setCityNameError("")
    setCityIdError("")
    setIdOfAttractionCHasHashtagError("")
    setIdOfHashtafCHasHashtagError("")
    setIdOfAttractionDHasHashtagError("")
    setIdOfHashtafDHasHashtagError("")
    setIdOfAttractionCHasActivityError("")
    setIdOfActivityCHasActivityError("")
    setIdOfAttractionDHasActivityError("")
    setIdOfActivityDHasActivityError("")
    setIdOfAttractionCHasAttractionError("")
    setIdOfCityCHasAttractionError("")
    setIdOfAttractionDHasAttractionError("")
    setIdOfCityDHasAttractionError("")


  };
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
    cleanErrors()
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
            
                  if (responce.data["errors"]["name"])
                    setNameError(responce.data["errors"]["name"]);

                  if (responce.data["errors"]["latitude"])
                    setLatitudeError(responce.data["errors"]["latitude"]);
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
          if(responce.status===206){
            setIdOfAttractionDeleteError(responce.data["errors"])
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
          if(responce.status===206){
            setHashtagNameError(responce.data["errors"]["name"])
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
          }
          if(responce.status===206){
            console.log(responce.data);
            setHashtagIdError(responce.data["errors"]);
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
          if(responce.status===206){
            console.log(responce.data)
            setActivityNameError(responce.data["errors"]["name"])
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
          if(responce.status==206){
            setActivityIdError(responce.data["errors"])
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
          if(responce.status===206){
            console.log(responce.data);
            setCityNameError(responce.data["errors"]["name"]);
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
          if(responce.status===206){
            console.log(responce.data)
            setCityIdError(responce.data["errors"])
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
          if(responce.status===206){
            console.log(responce.data)
            let attractionIdErrors=responce.data["errors"]["idOfAttraction"]
           if(attractionIdErrors){
           let joinedStringWithNewLine = attractionIdErrors.join("\n");
            setIdOfAttractionCHasHashtagError(joinedStringWithNewLine);}

           let hashtagIdErrors = responce.data["errors"]["idOfHashtag"]
           console.log(hashtagIdErrors);

           if(hashtagIdErrors){
           let joinedStringWithNewLine = hashtagIdErrors.join("\n");
             setIdOfHashtafCHasHashtagError(joinedStringWithNewLine);}
           



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
          if (responce.status === 206) {
            console.log(responce.data);
            if(responce.data["errors"]["idOfAttraction"])
              setIdOfAttractionDHasHashtagError(
                responce.data["errors"]["idOfAttraction"]
              );
            if(responce.data["errors"]["idOfHashtag"])
              setIdOfHashtafDHasHashtagError(
                responce.data["errors"]["idOfHashtag"]
              );

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
          if (responce.status === 206) {
            console.log(responce.data);
            if(responce.data["errors"]["idOfAttraction"])
              setIdOfAttractionCHasActivityError(responce.data["errors"]["idOfAttraction"])

            if(responce.data["errors"]["idOfActivity"])
              setIdOfActivityCHasActivityError(
                responce.data["errors"]["idOfActivity"]
              );

          }
        })
        .catch((error) => {
          console.error("Error:", error);
        });
    } else if (pickedAction == "deleteHAS_ACTIVITY") {
      axios
        .delete(
          `http://127.0.0.1:5000/admin/deleteRelationship_HAS_ACTIVITY/${idOfAttractionDHasActivity}/${idOfActivityDHasActivity}`,
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
            // setidOfActivityDHasActivity("")
          }
          if(responce.status===206)
          {
            console.log(responce.data);
            if(responce.data["errors"]["idOfAttraction"])
             setIdOfAttractionDHasActivityError(
               responce.data["errors"]["idOfAttraction"]
             );


            if (responce.data["errors"]["idOfActivity"])
              setIdOfActivityDHasActivityError(
                responce.data["errors"]["idOfActivity"]
              );

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
          if(responce.status===206){
            console.log(responce.data)
            if(responce.data['errors']['idOfAttraction'])
              setIdOfAttractionCHasAttractionError(responce.data['errors']['idOfAttraction'])

            if(responce.data['errors']['idOfCity'])
              setIdOfCityCHasAttractionError(
              responce.data["errors"]["idOfCity"]
            );
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
          if (responce.status === 206) {
            console.log(responce.data);
            if (responce.data["errors"]["idOfAttraction"])
              setIdOfAttractionDHasAttractionError(
                responce.data["errors"]["idOfAttraction"]
              );

            if (responce.data["errors"]["idOfCity"])
              setIdOfCityDHasAttractionError(
                responce.data["errors"]["idOfCity"]
              );
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
                validateStatus={nameError ? "error" : ""}
                help={nameError}
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
                onChange={(e) => {
                  const value = parseFloat(e.target.value);
                  if (!isNaN(value) && value >= -180 && value <= 180) {
                    setLongitude(value);
                  }
                }}
                rules={[
                  {
                    required: true,
                    message: "Please input longitude!",
                  },
                  {
                    validator: (_, value) => {
                      const numericValue = parseFloat(value);
                      if (isNaN(numericValue)) {
                        return Promise.reject(
                          new Error("Please enter a valid number.")
                        );
                      }
                      if (numericValue < -180 || numericValue > 180) {
                        return Promise.reject(
                          new Error("Longitude must be between -180 and 180.")
                        );
                      }
                      return Promise.resolve();
                    },
                  },
                ]}
              >
                <Input min={-180} max={180} type="number" />
              </Form.Item>
              <Form.Item
                label="Latitude"
                name="latitude"
                value={latitude}
                onChange={(e) => {
                  const value = parseFloat(e.target.value);
                  if (!isNaN(value) && value >= -90 && value <= 90) {
                    setLatitude(value);
                  }
                }}
                rules={[
                  {
                    required: true,
                    message: "Please input longitude!",
                  },
                  {
                    validator: (_, value) => {
                      const numericValue = parseFloat(value);
                      if (isNaN(numericValue)) {
                        return Promise.reject(
                          new Error("Please enter a valid number.")
                        );
                      }
                      if (numericValue < -90 || numericValue > 90) {
                        return Promise.reject(
                          new Error("Longitude must be between -90 and 90.")
                        );
                      }
                      return Promise.resolve();
                    },
                  },
                ]}
                validateStatus={latitudeError ? "error" : ""}
                help={latitudeError}
              >
                <Input min={-90} max={90} type="number" />
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
              validateStatus={idOfAttractionDeleteError ? "error" : ""}
              help={idOfAttractionDeleteError}
            >
              <Input />
            </Form.Item>
            {/* {idOfAttractionDelete && (
              <p style={{ marginLeft :"25vw",fontSize: "12px", color: "red" }}>
                {idOfAttractionDeleteError}
              </p>
            )} */}
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
              validateStatus={hashtagNameError ? "error" : ""}
              help={hashtagNameError}
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
              validateStatus={hashtagIdError ? "error" : ""}
              help={hashtagIdError}
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
              validateStatus={activityNameError ? "error" : ""}
              help={activityNameError}
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
              validateStatus={activityIdError ? "error" : ""}
              help={activityIdError}
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
              validateStatus={cityNameError ? "error" : ""}
              help={cityNameError}
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
              validateStatus={cityIdError ? "error" : ""}
              help={cityIdError}
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
              validateStatus={idOfAttractionCHasHashtagError ? "error" : ""}
              help={idOfAttractionCHasHashtagError}
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
              validateStatus={idOfHashtafCHasHashtagError ? "error" : ""}
              help={idOfHashtafCHasHashtagError}
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
              validateStatus={idOfAttractionDHasHashtagError ? "error" : ""}
              help={idOfAttractionDHasHashtagError}
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
              validateStatus={idOfHashtafDHasHashtagError ? "error" : ""}
              help={idOfHashtafDHasHashtagError}
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
              validateStatus={idOfAttractionCHasActivityError ? "error" : ""}
              help={idOfAttractionCHasActivityError}
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
              validateStatus={idOfActivityCHasActivityError ? "error" : ""}
              help={idOfActivityCHasActivityError}
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
              validateStatus={idOfAttractionDHasActivityError ? "error" : ""}
              help={idOfAttractionDHasActivityError}
            >
              <Input />
            </Form.Item>

            <Form.Item
              label="Id of activity"
              name="idOfActivity"
              value={idOfActivityDHasActivity}
              onChange={(e) => setIdOfActivityDHasActivity(e.target.value)}
              rules={[
                {
                  required: true,
                  message: "Please input id!",
                },
              ]}
              validateStatus={idOfActivityDHasActivityError ? "error" : ""}
              help={idOfActivityDHasActivityError}
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
              validateStatus={idOfAttractionCHasAttractionError ? "error" : ""}
              help={idOfAttractionCHasAttractionError}
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
              validateStatus={idOfCityCHasAttractionError ? "error" : ""}
              help={idOfCityCHasAttractionError}
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
              validateStatus={idOfAttractionDHasAttractionError ? "error" : ""}
              help={idOfAttractionDHasAttractionError}
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
              validateStatus={idOfCityDHasAttractionError ? "error" : ""}
              help={idOfCityDHasAttractionError}
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
    </>
  );
};
export default Admin;
