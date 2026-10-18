import { ScrollView, StyleSheet, Text, View } from 'react-native';
import DetailHeader, { detailTopInset } from '../components/DetailHeader';

const BG = '#07070a';
const TEXT = '#f4f4f5';
const MUTED = '#a1a1aa';

export default function SessionDetail({ session, onClose }) {
  const title = (session && session.title) || 'Session';
  const inset = detailTopInset();
  return (
    <View style={styles.root}>
      <ScrollView
        testID="session-scroll"
        style={styles.scroll}
        contentContainerStyle={[styles.measure, { paddingTop: 78 + inset }]}
      >
        <Text style={styles.kicker}>{session && session.num ? session.num : ''}</Text>
        <Text style={styles.title}>{title}</Text>
      </ScrollView>
      <DetailHeader
        onClose={onClose}
        title={title}
        closeTestID="session-close"
        shareTestID="session-share"
      />
    </View>
  );
}

const styles = StyleSheet.create({
  root: { flex: 1, backgroundColor: BG },
  scroll: { flex: 1 },
  measure: { paddingHorizontal: 22, paddingBottom: 48 },
  kicker: {
    color: MUTED,
    fontSize: 13,
    letterSpacing: 2,
    fontWeight: '500',
    marginBottom: 12,
  },
  title: { color: TEXT, fontSize: 28, lineHeight: 36, fontWeight: '600' },
});
