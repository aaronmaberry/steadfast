import { ScrollView, StyleSheet, Text } from 'react-native';
import content from '@steadfast/content';

const navy = '#0B1F38';
const bone = '#E6DDCC';

export default function DailyScreen() {
  const day1 = content.day1 || {};
  const body = day1.body || [];
  return (
    <ScrollView style={styles.sheet} contentContainerStyle={styles.inner}>
      <Text style={styles.kicker}>Daily</Text>
      <Text style={styles.title}>{day1.heading || day1.title || 'Sit down'}</Text>
      {body.map((para) => (
        <Text key={para} style={styles.body}>{para}</Text>
      ))}
      <Text style={styles.note}>Free. Training stays locked.</Text>
    </ScrollView>
  );
}

const styles = StyleSheet.create({
  sheet: { flex: 1, backgroundColor: bone },
  inner: { paddingHorizontal: 20, paddingTop: 20, paddingBottom: 36 },
  kicker: { fontSize: 12, letterSpacing: 2, color: navy, marginBottom: 8 },
  title: { fontSize: 32, fontWeight: '700', color: navy, marginBottom: 12 },
  body: { fontSize: 18, lineHeight: 28, color: navy, marginBottom: 12 },
  note: { fontSize: 14, color: navy, marginTop: 8 },
});
