import { useMemo, useState } from 'react';
import { Modal, Pressable, ScrollView, StyleSheet, Text } from 'react-native';
import { feed, pickDailyItem } from '../lib/dailyFeed';
import DailyReader from './DailyReader';

const navy = '#0B1F38';
const bone = '#E6DDCC';

export default function DailyScreen() {
  const item = useMemo(function () { return pickDailyItem(feed.items); }, []);
  const [open, setOpen] = useState(false);
  return (
    <ScrollView style={styles.sheet} contentContainerStyle={styles.inner}>
      <Text style={styles.kicker}>Daily</Text>
      <Text style={styles.title}>{item ? (item.silentTitle || item.title || 'Daily walk') : 'Daily walk'}</Text>
      <Text style={styles.verse}>{item && item.verseRef ? item.verseRef : ''}</Text>
      <Pressable
        testID="open-reading"
        accessibilityRole="button"
        accessibilityLabel="Open the reading"
        onPress={function () { setOpen(true); }}
        style={styles.open}
      >
        <Text style={styles.openText}>Open the reading</Text>
      </Pressable>
      <Text style={styles.note}>Free. Training stays locked.</Text>
      <Modal visible={open} animationType="none" onRequestClose={function () { setOpen(false); }}>
        <DailyReader item={item} onClose={function () { setOpen(false); }} />
      </Modal>
    </ScrollView>
  );
}

const styles = StyleSheet.create({
  sheet: { flex: 1, backgroundColor: bone },
  inner: { paddingHorizontal: 20, paddingTop: 20, paddingBottom: 36 },
  kicker: { fontSize: 12, letterSpacing: 2, color: navy, marginBottom: 8 },
  title: { fontSize: 32, fontWeight: '700', color: navy, marginBottom: 12 },
  verse: { fontSize: 16, lineHeight: 24, color: navy, marginBottom: 16 },
  open: { minHeight: 44, justifyContent: 'center', alignSelf: 'flex-start' },
  openText: { fontSize: 16, color: navy, textDecorationLine: 'underline' },
  note: { fontSize: 14, color: navy, marginTop: 18 },
});
