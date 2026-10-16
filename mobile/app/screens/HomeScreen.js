import { ScrollView, StyleSheet, Text } from 'react-native';
import content from '@steadfast/content';
import PlumbMark from '../components/PlumbMark';

const navy = '#0B1F38';
const bone = '#E6DDCC';

export default function HomeScreen() {
  const brand = content.brand || {};
  const hero = content.hero || {};
  const creed = brand.creed || content.creed;
  return (
    <ScrollView style={styles.sheet} contentContainerStyle={styles.inner}>
      <Text style={styles.steadfast}>{brand.steadfast || 'STEADFAST'}</Text>
      <Text style={styles.men}>{brand.men || 'MEN'}</Text>
      <Text style={styles.sub}>{brand.subtitle}</Text>
      <Text style={styles.author}>{brand.authorCaps || 'WES HART'}</Text>
      <PlumbMark color={navy} height={72} />
      <Text style={styles.line}>{hero.line}</Text>
      <Text style={styles.kicker}>{hero.kicker || 'THE FOUR MARKS'}</Text>
      <Text style={styles.creed}>{creed}</Text>
    </ScrollView>
  );
}

const styles = StyleSheet.create({
  sheet: { flex: 1, backgroundColor: bone },
  inner: { paddingHorizontal: 20, paddingTop: 24, paddingBottom: 36 },
  steadfast: {
    fontSize: 22,
    letterSpacing: 4,
    color: navy,
    textAlign: 'center',
    fontWeight: '700',
  },
  men: {
    fontSize: 36,
    letterSpacing: 6,
    color: navy,
    textAlign: 'center',
    fontWeight: '700',
    marginTop: 4,
  },
  sub: {
    fontSize: 18,
    fontStyle: 'italic',
    color: navy,
    textAlign: 'center',
    marginTop: 10,
  },
  author: {
    fontSize: 12,
    letterSpacing: 3,
    color: navy,
    textAlign: 'center',
    marginTop: 8,
    marginBottom: 8,
    fontWeight: '500',
  },
  line: {
    fontSize: 18,
    fontStyle: 'italic',
    color: navy,
    textAlign: 'center',
    marginTop: 16,
    marginBottom: 22,
  },
  kicker: {
    fontSize: 12,
    letterSpacing: 2,
    color: navy,
    fontWeight: '500',
    marginBottom: 10,
  },
  creed: { fontSize: 18, lineHeight: 28, color: navy },
});
