import { ScrollView, StyleSheet, Text } from 'react-native';
import content from '@steadfast/content';

const navy = '#0B1F38';
const bone = '#E6DDCC';

export default function StoreScreen() {
  const brand = content.brand || {};
  return (
    <ScrollView style={styles.sheet} contentContainerStyle={styles.inner}>
      <Text style={styles.title}>Store</Text>
      <Text style={styles.body}>The apps are free. No in-app purchase.</Text>
      <Text style={styles.note}>
        {brand.domain} ({brand.domainNote})
      </Text>
    </ScrollView>
  );
}

const styles = StyleSheet.create({
  sheet: { flex: 1, backgroundColor: bone },
  inner: { paddingHorizontal: 20, paddingTop: 20, paddingBottom: 36 },
  title: { fontSize: 32, fontWeight: '700', color: navy, marginBottom: 12 },
  body: { fontSize: 18, lineHeight: 28, color: navy, marginBottom: 16 },
  note: { fontSize: 14, color: navy },
});
