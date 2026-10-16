import { View } from 'react-native';

export default function PlumbMark({ color = '#E6DDCC', height = 64 }) {
  const cordW = Math.max(3, Math.round(height * 0.06));
  const cordH = Math.round(height * 0.32);
  const bob = Math.round(height * 0.28);
  return (
    <View style={{ alignItems: 'center', marginVertical: 8, height }}>
      <View style={{ width: cordW, height: cordH, backgroundColor: color }} />
      <View
        style={{
          width: bob,
          height: bob,
          borderRadius: bob / 2,
          backgroundColor: color,
          marginTop: -Math.round(bob * 0.12),
        }}
      />
      <View
        style={{
          width: 0,
          height: 0,
          marginTop: -Math.round(bob * 0.18),
          borderLeftWidth: Math.round(bob * 0.38),
          borderRightWidth: Math.round(bob * 0.38),
          borderTopWidth: Math.round(bob * 0.55),
          borderLeftColor: 'transparent',
          borderRightColor: 'transparent',
          borderTopColor: color,
        }}
      />
    </View>
  );
}
