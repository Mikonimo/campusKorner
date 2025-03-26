import React, { useState } from "react";
import axios from "axios";

const SubscribeForm = () => {
  const [email, setEmail] = useState("");
  const [firstName, setFirstName] = useState("");
  const [lastName, setLastName] = useState("");
  const [message, setMessage] = useState("");

  const handleSubmit = async (e) => {
    e.preventDefault();
    try {
      const response = await axios.post("http://localhost:5000/subscribe", {
        email,
        first_name: firstName,
        last_name: lastName,
      });
      setMessage("Subscription successful!");
    } catch (error) {
      setMessage("Error subscribing. Try again.");
    }
  };

  return (
    <div>
      <h2>Subscribe to Our Mailing List</h2>
      <form onSubmit={handleSubmit}>
        <input type="text" placeholder="First Name" value={firstName} onChange={(e) => setFirstName(e.target.value)} />
        <input type="text" placeholder="Last Name" value={lastName} onChange={(e) => setLastName(e.target.value)} />
        <input type="email" placeholder="Email Address" value={email} onChange={(e) => setEmail(e.target.value)} required />
        <button type="submit">Subscribe</button>
      </form>
      {message && <p>{message}</p>}
    </div>
  );
};

export default SubscribeForm;
