// src/components/ChatBot/ChatBot.jsx
import { useState } from 'react';
import './ChatBot.css';

const ChatBot = () => {
  const [messages, setMessages] = useState([]);
  const [inputText, setInputText] = useState('');
  const [currentStep, setCurrentStep] = useState(0);
  const [userData, setUserData] = useState({
    firstName: '',
    lastName: '',
    email: '',
    phone: '',
    purpose: '',
    preferredDate: ''
  });

  const steps = [
    { question: "Let's schedule your appointment! First, what's your first name?", field: 'firstName' },
    { question: "Great! And your last name?", field: 'lastName' },
    { question: "What's the best email to reach you?", field: 'email' },
    { question: "Please share your phone number:", field: 'phone' },
    { question: "What's the purpose of the appointment?", field: 'purpose' },
    { question: "Finally, what's your preferred date and time?", field: 'preferredDate' },
  ];

  const handleSubmit = async (e) => {
    e.preventDefault();
    if (!inputText.trim()) return;

    // Add user message
    const newMessages = [...messages, { text: inputText, isBot: false }];
    setMessages(newMessages);
    setInputText('');

    // Update user data
    if (currentStep < steps.length) {
      setUserData(prev => ({ ...prev, [steps[currentStep].field]: inputText }));
    }

    // Bot response
    if (currentStep < steps.length - 1) {
      setTimeout(() => {
        setMessages(prev => [...prev, { text: steps[currentStep + 1].question, isBot: true }]);
        setCurrentStep(prev => prev + 1);
      }, 1000);
    } else {
      setTimeout(() => {
        setMessages(prev => [...prev, { 
          text: `Please review your information:\n\n${Object.entries(userData).map(([key, value]) => `${key}: ${value}`).join('\n')}\n\nSubmit appointment request?`, 
          isBot: true 
        }]);
      }, 1000);
    }
  };

  return (
    <div className="chatbot-container">
      <div className="chatbot-header">
        <h1>Schedule Appointment</h1>
        <p>Let's find the perfect time for your visit!</p>
      </div>

      <div className="chat-messages">
        {messages.map((msg, index) => (
          <div key={index} className={`message ${msg.isBot ? 'bot' : 'user'}`}>
            {msg.text.split('\n').map((line, i) => <p key={i}>{line}</p>)}
          </div>
        ))}
      </div>

      <form onSubmit={handleSubmit} className="chat-input">
        <input
          type="text"
          value={inputText}
          onChange={(e) => setInputText(e.target.value)}
          placeholder="Type your response here..."
        />
        <button type="submit">Send</button>
      </form>
    </div>
  );
};

export default ChatBot;