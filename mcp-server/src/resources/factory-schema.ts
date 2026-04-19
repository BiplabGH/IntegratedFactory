export const FACTORY_SCHEMA = {
  machines: {
    types: ['cnc', 'conveyor', 'robot_arm'],
    idPattern: '{type}_{3-digit-number}',
    example: 'cnc_001',
  },
  mqttTopics: {
    pattern: 'factory/machines/{type}/{id}',
    uns: 'factory/{enterprise}/{site}/{area}/{line}/{machine}/{datatype}',
  },
  kafkaTopics: [
    'factory.machines.cnc',
    'factory.machines.conveyor',
    'factory.machines.robot',
    'factory.aggregated.metrics',
    'factory.alerts',
  ],
  metrics: {
    cnc: ['spindle_speed_rpm', 'feed_rate_mm_min', 'tool_wear_percent', 'coolant_temp_c', 'vibration_mm_s'],
    conveyor: ['belt_speed_m_min', 'load_kg', 'motor_temp_c', 'items_on_belt'],
    robot_arm: ['payload_kg', 'cycle_time_s', 'gripper_force_n'],
  },
} as const;
