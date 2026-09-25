import { ScrollView, StyleSheet, Text, View } from 'react-native';
import content from '@steadfast/content';

const navy = '#0B1F38';
const bone = '#E6DDCC';
const hair = '#484E46';

export default function TrainingScreen() {
  const sessions = (content.sessions || []).slice(0, 3);
  const mobile = content.mobile || {};
  return (
    <ScrollView style={styles.sheet} contentContainerStyle={styles.inner}>
      <Text style={styles.kicker}>STEADFAST MEN</Text>
      <Text style={styles.title}>Training</Text>
      <Text style={styles.lede}>{mobile.trainingLede || 'Three sessions. Sit down.'}</Text>
      {sessions.map((s) => (
        <View key={s.num} style={styles.row}>
          <Text style={styles.num}>{s.num}</Text>
          <Text style={styles.session}>{s.title}</Text>
        </View>
      ))}
    </ScrollView>
  );
}

const styles = StyleSheet.create({
  sheet: { flex: 1, backgroundColor: bone },
  inner: { paddingHorizontal: 20, paddingTop: 20, paddingBottom: 36 },
  kicker: {
    fontSize: 12,
    letterSpacing: 2,
    color: navy,
    fontWeight: '500',
    marginBottom: 6,
  },
  title: { fontSize: 32, fontWeight: '700', color: navy, marginBottom: 6 },
  lede: { fontSize: 16, fontStyle: 'italic', color: navy, marginBottom: 18 },
  row: {
    flexDirection: 'row',
    alignItems: 'center',
    minHeight: 44,
    borderBottomWidth: 1,
    borderBottomColor: hair,
    paddingVertical: 12,
    gap: 12,
  },
  num: { fontSize: 14, fontWeight: '500', color: navy, letterSpacing: 1, width: 28 },
  session: { fontSize: 18, color: navy, flex: 1 },
});
